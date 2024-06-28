"""
This module contains Python wrappers for PAL preprocessing algorithms.

The following classes and functions are available:

    * :class:`BSTS`

"""

#pylint: disable=line-too-long, unused-variable, too-many-lines, attribute-defined-outside-init
#pylint: disable=broad-except, no-member, too-many-arguments, too-many-local, too-many-branches
import logging
import uuid
from hdbcli import dbapi
from hana_ml.algorithms.pal.tsa.permutation_importance import PermutationImportanceMixin
from hana_ml.ml_exceptions import FitIncompleteError
from hana_ml.algorithms.pal.sqlgen import trace_sql
from hana_ml.algorithms.pal.tsa.utility import _convert_index_from_timestamp_to_int, _is_index_int
from hana_ml.algorithms.pal.tsa.utility import _get_forecast_starttime_and_timedelta
from hana_ml.dataframe import DataFrame
from hana_ml.visualizers.report_builder import Page
from hana_ml.visualizers.time_series_report import BSTSExplainer
from ..pal_base import (
    PALBase,
    ParameterTable,
    ListOfStrings,
    pal_param_register,
    require_pal_usable,
    quotename,
    execute_logged,
    try_drop
)
logger = logging.getLogger(__name__)#pylint: disable=invalid-name

class BSTS(PALBase, PermutationImportanceMixin):#pylint:disable=too-many-instance-attributes
    r"""
    class for Bayesian structure time-series(BSTS). Basically, let :math:`y_t` denote the
    observed value at time t in a real-valued time-series, a generic structural time series model
    can be described by a pair of equations relating :math:`y_t` to a vector of latent state
    variables :math:`\alpha_t` as follows:

        - :math:`y_t = Z_t^T\alpha_t + \epsilon_t, \epsilon_t\sim N(0, H_t)`
        - :math:`\alpha_t = T_t\alpha_t + R_t\eta_t, \eta_t \sim N(0, Q_t)`

    In this class, a special structural time-series model is considered, with system equation stated
    as follows:

        - :math:`y_t = \mu_t + \tau_t + \beta^T \bf{x}_t + \epsilon_t`,
        - :math:`\mu_t = \mu_{t-1} + \delta_t + u_t`,
        - :math:`\delta_t = \delta_{t-1} + v_t`,
        - :math:`\tau_t = -\sum_{s=1}^{S-1}\tau_{t-s} + w_t`,

    where :math:`\mu_t, \delta_t, \tau_t` and :math:`\beta^T\bf{x}_t` are the trend, slope of trend,
    seasonal(with period S) and regression components w.r.t. contemporaneous data, respectively,
    :math:`\epsilon_t, u_t, v_t` and :math:`w_t` are independent Gaussian random variables.

    BSTS can be seen as a combination of three Bayesian methods altogether -
    Kalman filter, spike-and-slab regression and Bayesian model averaging. In particular,
    samples of model parameters are drawn from its posterior distributions using MCMC.

    Parameters
    ----------
    burn : float, optional
        Specifies the ratio of total MCMC draws that are neglected from the beginning.
        Ranging from 0 to 1. In other words, only the tail 1-``burn`` portion of the
        total MCMC draw is kept(in the model) for prediction.

        Defaults to 0.5.
    niter : int, optional
        Specifies the total number of MCMC draws.

        Defaults to 1000.
    seasonal_period : int, optional
        Specifies the value of seasonal period.

            - Negative value : Period determined automatically
            - 0 or 1 : Target time-series assumed non-seasonal
            - 2 or larger : The specified value of seasonal period

        Defaults to -1, i.e. determined automatically.
    expected_model_size : int, optional
        Specifies the number of contemporaneous data that are expected to be included in
        the model.

        Defaults to half of the number of contemporaneous data columns.

    Attributes
    ----------
    stats\_ : DataFrame
        Related statistics on the inclusion of contemporaneous data w.r.t. the target
        time-series, structured as follows:

            - 1st column : DATA_NAME, type NVARCHAR or NVARCHAR, indicating the
              (column) name of contemporaneous data.
            - 2nd column : INCLUSION_PROB, type DOUBLE, indicating the inclusion
              probability of each contemporaneous data column.
            - 3rd column : AVG_COEFF, type DOUBLE, indicating the average value of
              coefficients for each contemporaneous data column if included in the model.

    decompose\_ : DataFrame
        Decomposed components of the target time-series, structured as follows:

            - 1st column : TIME_STAMP, type INTEGER, representing the order of time-series
              and is sorted ascendingly.
            - 2nd column : TREND, type DOUBLE, representing the trend component.
            - 3rd column : SEASONAL, type DOUBLE, representing the seasonal component.
            - 4th column : REGRESSION, type DOUBLE, representing the regression component w.r.t.
              contemporaneous data.
            - 5th column : RANDOM, type DOUBLE, representing the random component.

    model\_ : DataFrame
        DataFrame containing the retained tail MCMC samples in a JSON string, structured as follows:

           - 1st column : ROW_INDEX, type INTEGER, indicating the ID of current row.
           - 2nd column : MODEL_CONTENT, type NVARCHAR, JSON string.

    permutation\_importance\_ : DataFrame

        The importance of exogenous variables as determined by permutation importance analysis.
        The attribute only appear when invoking get_permutation_importance() function after a trained model is obtained, structured as follows:

            - 1st column : PAIR, measure name.
            - 2nd column : NAME, exogenous regressor name.
            - 3rd column : VALUE, the importance of the exogenous regressor.

    Examples
    --------
    >>> data.collect()
        TIME_STAMP  TARGET_SERIES  FEATURE_01  FEATURE_02  ...  FEATURE_07  FEATURE_08  FEATURE_09  FEATURE_10
    0            0          2.536       1.488      -0.561  ...       0.300       1.750       0.498       0.073
    1            1          0.882       1.100      -0.992  ...       0.180      -0.011       0.264       0.584
    2            2         -0.077       1.155      -1.212  ...       0.119      -0.028       0.031       0.448
    3            3          0.135       0.530      -1.034  ...       0.727      -0.230      -0.143      -0.269
    4            4          0.373       0.698      -1.195  ...       0.598       0.625      -0.219      -1.006
    5            5         -0.437       0.441      -1.386  ...      -0.199      -0.401      -0.526      -1.124
    ...
    47          47          0.730      -0.282      -1.019  ...      -0.511      -1.127      -0.792      -0.368
    48          48         -0.181      -0.145      -0.585  ...      -0.939      -0.388      -1.062      -0.547
    49          49         -0.144      -0.120      -0.496  ...      -0.856      -1.313      -1.161       0.150

    >>> bt = BSTS(burn=0.6, expected_model_size=2, niter=2000, seasonal_period=12, seed=1)
    >>> bt.fit(data=data, key='TIME_STAMP')
    >>> bt.stats_.collect()
    >>> bt.stats_.collect()
        DATA_NAME  INCLUSION_PROB  AVG_COEFF
    0  FEATURE_08         0.48500   0.173861
    1  FEATURE_01         0.40250   0.437837
    2  FEATURE_07         0.24625   0.189362
    3  FEATURE_09         0.23375   0.081339
    4  FEATURE_02         0.19750   0.098693
    5  FEATURE_04         0.14375   0.130138
    6  FEATURE_06         0.14125   0.062544
    7  FEATURE_10         0.10375   0.003327
    8  FEATURE_03         0.08875   0.009415
    9  FEATURE_05         0.08750   0.021849

    >>> data_pred.collect()
       TIME_STAMP  FEATURE_01  FEATURE_02  FEATURE_03  ...  FEATURE_07  FEATURE_08  FEATURE_09  FEATURE_10
    0          50       0.471      -0.660      -0.086  ...      -1.107      -0.559      -1.404      -1.646
    1          51       0.872       0.062       0.481  ...      -0.729       0.894      -0.754       1.107
    2          52       0.976      -0.003       0.824  ...      -0.589       0.133       0.007      -0.115
    3          53       0.446       0.231       0.098  ...      -0.014       0.182      -0.465      -1.062
    4          54       0.248      -0.142       0.174  ...      -0.380       1.236      -0.552      -1.051
    5          55      -0.319      -0.867       0.334  ...      -0.160      -0.488      -0.650      -0.769
    6          56      -0.194      -0.822       0.523  ...      -0.566      -0.289      -0.596      -0.559
    7          57      -0.357      -0.564      -0.391  ...      -0.980       0.578      -0.948      -0.870
    8          58      -0.760      -1.113      -0.178  ...      -0.477      -0.705      -1.199      -0.517
    9          59      -0.611      -1.163       0.186  ...      -0.976      -0.576      -0.927      -1.577
    >>> forecast_, _ = bt.predict(data=data_pred, key='TIME_STAMP')
    >>> forecast_.collect()
       TIME_STAMP  FORECAST        SE  LOWER_80  UPPER_80  LOWER_95  UPPER_95
    0          50  0.143151  0.591231 -0.614542  0.900844 -1.015640  1.301943
    1          51  0.469405  0.765558 -0.511697  1.450508 -1.031060  1.969871
    2          52  0.155813  1.004786 -1.131872  1.443499 -1.813531  2.125158
    3          53  0.055188  1.160655 -1.432251  1.542627 -2.219653  2.330029
    4          54  0.064481  1.385078 -1.710569  1.839531 -2.650222  2.779185
    5          55  0.045844  1.660894 -2.082678  2.174365 -3.209448  3.301135
    6          56 -0.039227  1.905115 -2.480732  2.402277 -3.773185  3.694731
    7          57  0.124084  2.193157 -2.686560  2.934728 -4.174424  4.422592
    8          58 -0.200588  2.479858 -3.378655  2.977478 -5.061020  4.659843
    9          59  0.339182  2.763764 -3.202725  3.881089 -5.077696  5.756059
    """
    op_name = 'BSTS'
    def __init__(self,#pylint:disable=too-many-arguments
                 burn=None,
                 niter=None,
                 seasonal_period=None,
                 expected_model_size=None,
                 seed=None):
        if not hasattr(self, 'hanaml_parameters'):
            setattr(self, 'hanaml_parameters', pal_param_register())
        super(BSTS, self).__init__()#pylint:disable=super-with-arguments

        self.burn = self._arg('burn', burn, float)
        self.niter = self._arg('niter', niter, int)
        self.seasonal_period = self._arg('seasonal_period', seasonal_period, int)
        self.expected_model_size = self._arg('expected_model_size', expected_model_size, int)
        self.seed = self._arg('seed', seed, int)
        self.stats_ = None
        self.decompose_ = None
        self.model_ = None
        self.is_index_int = True

    @trace_sql
    def fit(self,#pylint:disable=too-many-statements, too-many-branches, too-many-locals
            data,
            key=None,
            endog=None,
            exog=None):
        r"""
        Python wrapper for the training procedure of PAL BSTS.

        Parameters
        ----------
        data : DataFrame

            Input data for BSTS, inclusive of timestamp, target series and
            contemporaneous data columns.

        key : str

            The timestamp column of data. The type of key column should be INTEGER,
            TIMESTAMP, DATE or SECONDDATE.

            Defaults to index column of ``data`` is ``data`` is indexed by a single column,
            otherwise it is mandatory.

        endog : str, optional

            The endogenous variable, i.e. the target time-series. The type of endog column could be
            INTEGER, DOUBLE or DECIMAL(p,s).

            Defaults to the first non-key column of ``data``.

        exog : str or a list of str, optional

            An optional array of exogenous variables, i.e. contemporaneous data columns.
            The type of exog column could be INTEGER, DOUBLE or DECIMAL(p,s).

            Defaults to all non-key, non-endog columns in ``data``.

        Returns
        -------
        A fitted object of class BSTS.
        """
        setattr(self, 'hanaml_fit_params', pal_param_register())
        setattr(self, "training_data", data)
        data = self._arg('data', data, DataFrame, required=True)
        conn = data.connection_context
        require_pal_usable(conn)
        if not self._disable_hana_execution:
            cols = data.columns
            index = data.index
            key = self._arg('key', key, str, not isinstance(index, str))
            if isinstance(index, str):
                if key is not None and index != key:
                    warn_msg = f"Discrepancy between the designated key column '{key}' " +\
                    f"and the designated index column '{index}'."
                    logger.warning(warn_msg)
            key = index if key is None else key
            cols.remove(key)
            endog = self._arg('endog', endog, str)
            if endog is None:
                endog = cols[0]
            cols.remove(endog)
            if isinstance(exog, str):
                exog = [exog]
            exog = self._arg('exog', exog, ListOfStrings)
            if exog is None:
                exog = cols

            setattr(self, 'key', key)
            setattr(self, 'endog', endog)
            setattr(self, 'exog', exog)

            data_ = data[[key, endog] + exog]
            self.is_index_int = _is_index_int(data_, key)#pylint:disable=attribute-defined-outside-init
            if not self.is_index_int:
                data_ = _convert_index_from_timestamp_to_int(data_, key)
            try:
                self.forecast_start, self.timedelta = _get_forecast_starttime_and_timedelta(data, key, self.is_index_int)#pylint:disable=attribute-defined-outside-init
            except Exception as err:#pylint:disable=bare-except
                logger.warning(err)
        else:
            data_ = data
        unique_id = str(uuid.uuid1()).replace('-', '_').upper()
        outputs = ['STATS', 'DECOMPOSE', 'MODEL']
        outputs = [f'#PAL_BSTS_{name}_TBL_{self.id}_{unique_id}' for name in outputs]
        stats_tbl, decompose_tbl, model_tbl = outputs
        param_rows = [('BURN_IN', None, self.burn, None),
                      ('EXPECTED_MODEL_SIZE', self.expected_model_size,
                       None, None),
                      ('SEASONAL_PERIOD', self.seasonal_period, None, None),
                      ('MAX_ITER', self.niter, None, None),
                      ('RANDOM_SEED', self.seed, None, None)]
        try:
            self._call_pal_auto(conn,
                                'PAL_BSTS_TRAIN',
                                data_,
                                ParameterTable().with_data(param_rows),
                                *outputs)

        except dbapi.Error as db_err:
            logger.exception(str(db_err))
            try_drop(conn, outputs)
            raise
        except Exception as db_err:
            logger.exception(str(db_err))
            try_drop(conn, outputs)
            raise
        self.stats_ = conn.table(stats_tbl)
        self.decompose_ = conn.table(decompose_tbl)
        if not self.is_index_int:
            dcols = self.decompose_.columns
            self.decompose_ = self.decompose_.alias('L').join(data.add_id(key + '(INT)',\
            ref_col=key)[[key, key + '(INT)']].alias('R'), 'L."TIME_STAMP"=R.%s'%(quotename(key + '(INT)')),\
            select=[key] + dcols[1:])
        self.model_ = conn.table(model_tbl)
        setattr(self, 'fit_data', data_)
        return self

    @trace_sql
    def predict(self,#pylint:disable=too-many-statements, too-many-branches, too-many-locals
                data=None,
                key=None,
                exog=None,
                horizon=None):
        r"""
        Python wrapper for the predict procedure of PAL BSTS.

        Parameters
        ----------
        data : DataFrame, optional

            Index and contemporaneous data for BSTS prediction.

            Required only if contemporaneous data is available in the training phase.

        key : str, optional

            The timestamp column of data, should be of type
            INTEGER, TIMESTAMP, DATE or SECONDDATE.

            Effective only when ``data`` is not None.

            Defaults to the index of ``data`` if ``data`` is indexed by a single column,
            otherwise it is mandatory.

        exog : str of list or str, optional
            An optional array of exogenous variables, i.e. contemporaneous data columns.
            The type of exog column could be INTEGER, DOUBLE or DECIMAL(p,s).

            Effective only when ``data`` is not None.

            Defaults to all non-key columns in ``data``.

        horizon : int, optional
            Number of predictions for future observations.

            Valid only when ``data`` is None.

            Defaults to 1.

        Returns
        -------
        DataFrame 1
            DataFrame containing the forecast values and other related
            statistics(like standard error estimation, upper/lower quantiles).

        DataFrame 2
            DataFrame containing the trend/seasonal/regression components
            w.r.t. the forecast values.
        """
        if getattr(self, 'model_') is None:
            raise FitIncompleteError()
        data = self._arg('data', data, DataFrame)
        horizon = self._arg('horizon', horizon, int)
        unique_id = str(uuid.uuid1()).replace('-', '_').upper()
        if data is not None:
            conn = data.connection_context

            index = data.index
            key = self._arg('key', key, str, not isinstance(index, str))
            if isinstance(index, str):
                if key is not None and index != key:
                    warn_msg = f"Discrepancy between the designated key column '{key}' " +\
                    f"and the designated index column '{index}'."
                    logger.warning(warn_msg)
            key = index if key is None else key
            if isinstance(exog, str):
                exog = [exog]
            exog = self._arg('exog', exog, ListOfStrings)
            cols = data.columns
            cols.remove(key)
            if exog is None:
                exog = cols
            data_ = data[[key] + exog]
            is_index_int = _is_index_int(data_, key)
            if not is_index_int:
                data_ = _convert_index_from_timestamp_to_int(data_, key)
        else:
            is_index_int = True
            conn = self.model_.connection_context
            data_tbl = f"#PAL_BSTS_FORECAST_DATA_TBL_{self.id}_{unique_id}"
            with conn.connection.cursor() as cur:
                execute_logged(cur,#pylint:disable=too-many-function-args
                               f'CREATE LOCAL TEMPORARY COLUMN TABLE {data_tbl}' +\
                               '("TIME_STAMP" INTEGER, "VAL" DOUBLE)',
                               conn.sql_tracer,
                               conn)
                data_ = conn.table(data_tbl)
            if not conn.connection.getautocommit():
                conn.connection.commit()
        out_tabs = ['FORECAST', 'DECOMPOSE']
        out_tabs = [f'#PAL_BSTS_PRED_{tb}_TBL_{self.id}_{unique_id}' for tb in out_tabs]
        param_rows = [('FORECAST_LENGTH', horizon, None, None)]
        setattr(self, 'predict_data', data_)
        try:
            self._call_pal_auto(conn,
                                'PAL_BSTS_PREDICT',
                                data_,
                                self.model_,
                                ParameterTable().with_data(param_rows),
                                *out_tabs)
        except dbapi.Error as db_err:
            logger.exception(str(db_err))
            try_drop(conn, out_tabs)
            raise
        except Exception as db_err:
            logger.exception(str(db_err))
            try_drop(conn, out_tabs)
            raise
        fct = conn.table(out_tabs[0])#forecast result
        dec = conn.table(out_tabs[1])#decompose result
        if not is_index_int:
            fcols = fct.columns
            fct = fct.alias('L').join(data.add_id(key + '(INT)',\
                  ref_col=key)[[key, key + '(INT)']].alias('R'),\
                  'L.%s=R.%s'%('TIME_STAMP', quotename(key + '(INT)')),\
                  select=[key] + fcols[1:])
            dcols = dec.columns
            dec = dec.alias('L').join(data.add_id(key + '(INT)',\
                  ref_col=key)[[key, key + '(INT)']].alias('R'),\
                  'L.%s=R.%s'%('TIME_STAMP', quotename(key + '(INT)')),\
                  select=[key] + dcols[1:])
        if data is not None:
            setattr(self, "forecast_result", fct)
            setattr(self, "reason_code", dec)
            return fct, dec
        if not self.is_index_int:
            min_dt = fct.min()['TIME_STAMP']
            fct = conn.sql("""
                           SELECT ADD_SECONDS('{0}', ({1} - {10}) * {2}) AS TIME_STAMP,
                           {4},
                           {5},
                           {6},
                           {7},
                           {8},
                           {9}
                           FROM ({3})
                           """.format(self.forecast_start,
                                      quotename(fct.columns[0]),
                                      self.timedelta,
                                      fct.select_statement,
                                      quotename(fct.columns[1]),
                                      quotename(fct.columns[2]),
                                      quotename(fct.columns[3]),
                                      quotename(fct.columns[4]),
                                      quotename(fct.columns[5]),
                                      quotename(fct.columns[6]),
                                      str(int(min_dt))))
            dec = conn.sql("""
                           SELECT ADD_SECONDS('{0}', ({1} - {7}) * {2}) AS TIME_STAMP,
                           {4},
                           {5},
                           {6}
                           FROM ({3})
                           """.format(self.forecast_start,
                                      quotename(dec.columns[0]),
                                      self.timedelta,
                                      dec.select_statement,
                                      quotename(dec.columns[1]),
                                      quotename(dec.columns[2]),
                                      quotename(dec.columns[3]),
                                      str(int(min_dt))))
        setattr(self, "forecast_result", fct)
        setattr(self, "reason_code", dec)
        return fct, dec

    def build_report(self):
        r"""
        Generate time series report.
        """
        from hana_ml.visualizers.time_series_report_template_helper import TimeSeriesTemplateReportHelper
        if self.key is None:
            self.key = self.training_data.columns[0]
        if self.endog is None:
            self.endog = self.training_data.columns[1]
        if len(self.training_data.columns) > 2:
            if self.exog is None:
                self.exog = self.training_data.columns
                self.exog.remove(self.key)
                self.exog.remove(self.endog)
        self.report = TimeSeriesTemplateReportHelper(self)
        pages = []
        page0 = Page("Forecast Result Analysis")
        tse = BSTSExplainer(key=self.key, endog=self.endog, exog=self.exog)
        tse.add_line_to_comparison_item("Training Data", data=self.training_data, x_name=self.key, y_name=self.endog)
        if hasattr(self, 'forecast_result'):
            if self.forecast_result:
                tse.add_line_to_comparison_item("Forecast Result",
                                                data=self.forecast_result,
                                                x_name=self.forecast_result.columns[0],
                                                y_name=self.forecast_result.columns[1])
                tse.add_line_to_comparison_item("SE",
                                                data=self.forecast_result,
                                                x_name=self.forecast_result.columns[0],
                                                y_name=self.forecast_result.columns[2],
                                                color='grey')
                tse.add_line_to_comparison_item('PI1', data=self.forecast_result, x_name=self.forecast_result.columns[0], confidence_interval_names=[self.forecast_result.columns[3], self.forecast_result.columns[4]],color="pink")
                tse.add_line_to_comparison_item('PI2', data=self.forecast_result, x_name=self.forecast_result.columns[0], confidence_interval_names=[self.forecast_result.columns[5], self.forecast_result.columns[6]],color="#ccc")
        page0.addItems(tse.get_comparison_item())
        pages.append(page0)
        if hasattr(self, 'reason_code'):
            if self.reason_code:
                page1 = Page("Explainability")
                try:
                    tse.set_forecasted_data(self.predict_data)
                    tse.set_forecasted_result_explainer(self.reason_code)
                    page1.addItems(tse.get_decomposition_items_from_forecasted_result())
                    page1.addItems(tse.get_summary_plot_items_from_forecasted_result())
                    page1.addItems(tse.get_force_plot_item_from_forecasted_result())
                except Exception as err:
                    logger.error(err)
                pages.append(page1)
        self.report.add_pages(pages)
        self.report.build_report()

    def generate_html_report(self, filename=None):
        """
        Display function.
        """
        self.report.generate_html_report(filename)

    def generate_notebook_iframe_report(self):
        """
        Display function.
        """
        self.report.generate_notebook_iframe_report()

    def get_permutation_importance(self, data, model=None, key=None, endog=None, exog=None, repeat_time=None, random_state=None, thread_ratio=None,
                                   partition_ratio=None, regressor_top_k=None, accuracy_measure=None, ignore_zero=None):
        """
        Please see :ref:`permutation_imp_ts-label` for details.
        """
        if key is None:
            key = self.key
        if endog is None:
            endog = self.endog
        if exog is None:
            exog = self.exog
        if model is None:
            if getattr(self, 'model_') is None:
                raise FitIncompleteError()
            model = self.model_
        if isinstance(model, str):
            model = model.lower()
            if model == 'rdt':
                model = None
            else:
                msg = "Permutation importance only supports 'rdt' as model free method!"
                logger.error(msg)
                raise ValueError(msg)

        if model is None:
            permutation_data = data[[key] + [endog] + exog]
            real_data=None
        else:
            permutation_data = data[[key] + exog]
            real_data = data[[key] + [endog]]

        is_index_int = _is_index_int(permutation_data, key)
        if not is_index_int:
            if model:
                permutation_data = _convert_index_from_timestamp_to_int(permutation_data, key)
                real_data = _convert_index_from_timestamp_to_int(real_data, key)
            if model is None:
                permutation_data = _convert_index_from_timestamp_to_int(permutation_data, key)
        return super()._get_permutation_importance(permutation_data, real_data, model, repeat_time, random_state, thread_ratio,
                                                   partition_ratio, regressor_top_k, accuracy_measure, ignore_zero)

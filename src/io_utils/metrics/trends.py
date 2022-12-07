import pandas as pd
import numpy as np
from io_utils.metrics.mktest import mk_test
from scipy.stats import theilslopes

def theilsen_slope(ds, alpha=0.05, mktest=True):
    '''
    implements a method for robust linear regression.
    It computes the slope as the median of all slopes between paired values.

    Parameters
    ----------
    ds: pd.Series
        Pandas time series
    alpha : float, optional
        Confidence degree between 0 and 1. Default is 95% confidence.
        Note that `alpha` is symmetric around 0.5, i.e. both 0.1 and 0.9 are
        interpreted as "find the 90% confidence interval".

    Returns
    -------
    slope_df : DataFrame
        DataFrame that contains the trends parameters
    '''

    theilsen_df = pd.DataFrame(index=['medslope', 'medintercept', 'lo_slope',
                                      'up_slope', 'ts_significance_mask'],
                               columns=df.columns.values)

    df['t'] = range(df.index.values.size)

    for i, col_name in enumerate(df.columns.values[df.columns.values != 't']):
        y = df[[col_name, 't']].dropna()[col_name].values
        if y.size == 0:
            medslope, medintercept, lo_slope, up_slope, n = np.nan, np.nan, np.nan, np.nan, 0
        else:
            t = df[[col_name, 't']].dropna()['t'].values
            try:
                medslope, medintercept, lo_slope, up_slope = theilslopes(y, t,
                                                                         alpha)
            except:
                medslope, medintercept, lo_slope, up_slope = np.nan, np.nan, np.nan, np.nan

        theilsen_df.at[('medslope', col_name)] = medslope
        theilsen_df.at[('medintercept', col_name)] = medintercept
        theilsen_df.at[('lo_slope', col_name)] = lo_slope
        theilsen_df.at[('up_slope', col_name)] = up_slope
        theilsen_df.at[('n_obs', col_name)] = y.size

        if (lo_slope > 0) and (up_slope > 0):
            theilsen_df.at[('ts_significance_mask', col_name)] = 1
        else:
            theilsen_df.at[('ts_significance_mask', col_name)] = 0

    return theilsen_df


def mannkendall(self, alpha=0.05):
    '''
    Mann Kendall test for detection of a significant trend.
    Also computes the linear regression slopes and intercepts.

    Parameters
    -------
    alpha : scalar, float, greater than zero
        significance level of the statistical test (Type I error)

    Returns
    -------
    mk_df : DataFrame
        DataFrame that contains the trends parameters
    '''
    df = self.df.copy()
    mk_df = pd.DataFrame(
        index=['mk_significance_mask', 'slope_linreg', 'intercept_linreg',
               'p_mk', 'mk_n_obs'],
        columns=df.columns.values)

    df['t'] = range(df.index.values.size)

    for i, col_name in enumerate(df.columns.values[df.columns.values != 't']):

        y = df[[col_name, 't']].dropna()[col_name].values
        t = df[[col_name, 't']].dropna()['t'].values

        try:
            y = y.astype(np.float32)
            mk, m, c, p = mk_test(t=t, x=y, eps=0, alpha=alpha, Ha='upordown')
        except:
            mk, m, c, p = np.nan, np.nan, np.nan, np.nan
        mk_df.at[('mk_significance_mask', col_name)] = 1 if mk == True else 0
        mk_df.at[('slope_linreg', col_name)] = m
        mk_df.at[('intercept_linreg', col_name)] = c
        mk_df.at[('p_mk', col_name)] = p
        mk_df.at[('mk_n_obs', col_name)] = y.size

    return mk_df

import pytest
import numpy as np
import pandas as pd
from dateutil.parser import parse as parse_date

from pdutils import df_compare, ndarray_compare, ts_compare, assert_, assert_not


#    Example pandas DataFrame objects that are expected to be equal.
TEST_DF_SAME = [
    (
        pd.DataFrame({'a': [1., 2., 3.], 'b': ['a', 'b', 'c']}),
        pd.DataFrame({'a': [1., 2., 3.], 'b': ['a', 'b', 'c']}),
    ),
    (
        pd.DataFrame({'a': [1., 2., 3.]}, pd.date_range('1970-01-01', periods=3, freq='S')),
        pd.DataFrame({'a': [1., 2., 3.]}, pd.date_range('1970-01-01', periods=3, freq='S')),
    ),
    (
        pd.DataFrame({'a': [1., 2., 3.]}, pd.date_range('1970-01-01', periods=3, freq='S')),
        pd.DataFrame({'a': [1., 2., 3.]}, pd.date_range('1970-01-01', periods=3, freq='S')),
    ),
    (
        pd.DataFrame({'a': [1., 2., 3.], 'b': [1, 2, 3]}, pd.date_range('1970-01-01', periods=3, freq='S')),
        pd.DataFrame({'a': [1., 2., 3.], 'b': [1, 2, 3]}, pd.date_range('1970-01-01', periods=3, freq='S')),
    ),
    (
        pd.DataFrame({'a': [1., 2., 3.], 'b': [1, 2, 3]}, pd.date_range('1970-01-01', periods=3, freq='S')),
        pd.DataFrame({'a': [1., 2., 3.], 'b': [1, 2, 3]}, pd.date_range('1970-01-01', periods=3, freq='S'),
                     columns=['b', 'a']),
    ),
    (
        pd.DataFrame({'a': [np.nan, 2., 3.]}, pd.date_range('1970-01-01', periods=3, freq='S')),
        pd.DataFrame({'a': [np.nan, 2., 3.]}, pd.date_range('1970-01-01', periods=3, freq='S')),
    ),
]


#    Example pandas DataFrame objects that are not expected to be equal.
TEST_DF_DIFFERENT = [
    (
        pd.DataFrame({'a': [1., 2., 3.], 'b': ['a', 'b', 'c']}),
        pd.DataFrame({'a': [1., 2., 3.], 'b': ['a', 'b', 'd']}),
    ),
    (
        pd.DataFrame({'a': [1., 2., 3.], 'b': ['a', 'b', 'c']}),
        pd.DataFrame({'a': [1., 2., 4.], 'b': ['a', 'b', 'c']}),
    ),
    (
        pd.DataFrame({'a': [1., 2., 3.], 'b': ['a', 'b', 'c']}),
        pd.DataFrame({'a': [1., 2., 4.], 'b': ['a', 'b', 'c']}, pd.date_range('1970-01-01', periods=3, freq='S')),
    ),
    (
        pd.DataFrame({'a': [1., 2.]}, pd.date_range('1970-01-01', periods=2, freq='S')),
        pd.DataFrame({'a': [np.nan, 2., 3.]}, pd.date_range('1970-01-01', periods=3, freq='S')),
    ),
    (
        pd.DataFrame({'a': [1., 2., 3.]}, pd.date_range('1970-01-01', periods=3, freq='S')),
        pd.DataFrame({'a': [1., 2., 3.], 'b': [1., 2., 3.]}, pd.date_range('1970-01-01', periods=3, freq='S')),
    ),
    (
        pd.DataFrame({'a': [1., 2., 3.], 'b': [1., 2., 3.]}, pd.date_range('1970-01-01', periods=3, freq='S')),
        pd.DataFrame({'a': [1., 2., 3.], 'c': [1., 2., 3.]}, pd.date_range('1970-01-01', periods=3, freq='S')),
    ),
    (
        pd.DataFrame({'a': [1., 2., 3.]}, pd.date_range('1970-01-01', periods=3, freq='S')),
        pd.DataFrame({'a': [np.nan, 2., 3.]}, pd.date_range('1970-01-01', periods=3, freq='S')),
    ),
    (
        pd.DataFrame({'a': [2., np.nan, 3.]}, pd.date_range('1970-01-01', periods=3, freq='S')),
        pd.DataFrame({'a': [np.nan, 2., 3.]}, pd.date_range('1970-01-01', periods=3, freq='S')),
    ),
    (
        pd.DataFrame({'a': [1., 2., 3.]}, pd.date_range('1970-01-01', periods=3, freq='S')),
        pd.DataFrame({'a': [True, False, True]}, pd.date_range('1970-01-01', periods=3, freq='S')),
    ),
    (
        pd.DataFrame({'a': [1., 2., 3.]}, pd.date_range('1970-01-01', periods=3, freq='S')),
        pd.DataFrame({'a': [1., 2., 3.]}, [0, 1, 2]),
    ),
    (
        pd.DataFrame({'a': [1., 2., 3.]}, pd.date_range('1970-01-01', periods=3, freq='S')),
        pd.DataFrame({'a': [1., 2., 3.]}, pd.date_range('1970-01-01', periods=3, freq='D')),
    ),
]


#    Example numpy ndarray objects that are expected to be equal.
TEST_NDARRAY_SAME = [
    (np.array([]), np.array([])),
    (np.array([[]]), np.array([[]])),
    (np.array([[1, 2, 3], [4, 5, 6]]), np.array([[1, 4], [2, 5], [3, 6]]).T),
    (np.array([True, False, True]), np.array([True, False, True])),
    (np.array(['a', 'b', 'c']), np.array(['a', 'b', 'c'])),
    (
        np.array([parse_date('2013-01-01'), parse_date('2013-01-02'), parse_date('2013-01-03')]),
        np.array([parse_date('2013-01-01'), parse_date('2013-01-02'), parse_date('2013-01-03')]),
    ),
    (np.array([1., 2., 3.]), np.array([1., 2., 3.])),
    (np.array([1., 2., np.nan]), np.array([1., 2., np.nan])),
]


#    Example numpy ndarray objects that are not expected to be equal.
TEST_NDARRAY_DIFFERENT = [
    (np.array([]), np.array([1])),
    (np.array([[]]), np.array([1])),
    (np.array([[1, 2, 3], [4, 5, 6]]), np.array([[1, 4], [2, 5], [3, 6]])),
    (np.array([1, 2, 3]), np.array([1, 2, 4])),
    (np.array([True, False, True]), np.array([True, True, True])),
    (np.array(['a', 'b', 'c']), np.array(['a', 'b', 'd'])),
    (
        np.array([parse_date('2013-01-01'), parse_date('2013-01-02'), parse_date('2013-01-03')]),
        np.array([parse_date('2013-01-01'), parse_date('2013-01-02'), parse_date('2013-01-04')]),
    ),
    (np.array([1., 2., 3.]), np.array([1, 2, 3])),
    (np.array([1., 2., np.nan]), np.array([1., np.nan, 2.])),
    (np.array([1., 2., np.nan]), np.array([1., 3., np.nan])),
]


#    Example pandas TimeSeries objects that are expected to be equal.
TEST_TS_SAME = [
    (
        pd.TimeSeries([1., 2., 3.], pd.date_range('1970-01-01', periods=3, freq='S')),
        pd.TimeSeries([1., 2., 3.], pd.date_range('1970-01-01', periods=3, freq='S')),
    ),
    (
        pd.TimeSeries([1, 2, 3], pd.date_range('1970-01-01', periods=3, freq='S')),
        pd.TimeSeries([1, 2, 3], pd.date_range('1970-01-01', periods=3, freq='S')),
    ),
    (
        pd.TimeSeries([np.nan, 2., 3.], pd.date_range('1970-01-01', periods=3, freq='S')),
        pd.TimeSeries([np.nan, 2., 3.], pd.date_range('1970-01-01', periods=3, freq='S')),
    ),
]


#    Example pandas TimeSeries objects that are not expected to be equal.
TEST_TS_DIFFERENT = [
    (
        pd.TimeSeries([1., 2.], pd.date_range('1970-01-01', periods=2, freq='S')),
        pd.TimeSeries([np.nan, 2., 3.], pd.date_range('1970-01-01', periods=3, freq='S')),
    ),
    (
        pd.TimeSeries([1., 2., 3.], pd.date_range('1970-01-01', periods=3, freq='S')),
        pd.TimeSeries([np.nan, 2., 3.], pd.date_range('1970-01-01', periods=3, freq='S')),
    ),
    (
        pd.TimeSeries([2., np.nan, 3.], pd.date_range('1970-01-01', periods=3, freq='S')),
        pd.TimeSeries([np.nan, 2., 3.], pd.date_range('1970-01-01', periods=3, freq='S')),
    ),
    (
        pd.TimeSeries([1., 2., 3.], pd.date_range('1970-01-01', periods=3, freq='S')),
        pd.TimeSeries([True, False, True], pd.date_range('1970-01-01', periods=3, freq='S')),
    ),
    (
        pd.TimeSeries([1., 2., 3.], pd.date_range('1970-01-01', periods=3, freq='S')),
        pd.TimeSeries([1., 2., 3.], [0, 1, 2]),
    ),
    (
        pd.TimeSeries([1., 2., 3.], pd.date_range('1970-01-01', periods=3, freq='S')),
        pd.TimeSeries([1., 2., 3.], pd.date_range('1970-01-01', periods=3, freq='D')),
    ),
]


@pytest.mark.parametrize(('df1', 'df2'), TEST_DF_SAME)
def test_df_compare_same(df1, df2):
    assert_(df_compare(df1, df2))


@pytest.mark.parametrize(('df1', 'df2'), TEST_DF_DIFFERENT)
def test_df_compare_different(df1, df2):
    assert_not(df_compare(df1, df2))


@pytest.mark.parametrize(('a1', 'a2'), TEST_NDARRAY_SAME)
def test_ndarray_compare_same(a1, a2):
    assert_(ndarray_compare(a1, a2))


@pytest.mark.parametrize(('a1', 'a2'), TEST_NDARRAY_DIFFERENT)
def test_ndarray_compare_different(a1, a2):
    assert_not(ndarray_compare(a1, a2))


@pytest.mark.parametrize(('ts1', 'ts2'), TEST_TS_SAME)
def test_ts_compare_same(ts1, ts2):
    assert_(ts_compare(ts1, ts2))


@pytest.mark.parametrize(('ts1', 'ts2'), TEST_TS_DIFFERENT)
def test_ts_compare_different(ts1, ts2):
    assert_not(ts_compare(ts1, ts2))


@pytest.mark.parametrize(('df1', 'df2', 'tolerance'), [
    (
        pd.DataFrame({'a': [1., 2., 3.]}, pd.date_range('1970-01-01', periods=3, freq='S')),
        pd.DataFrame({'a': [1.0001, 2.0002, 3.]}, pd.date_range('1970-01-01', periods=3, freq='S')),
        1e-4,   # tolerance
    ),
    (
        pd.DataFrame({'a': [1., 2., 3.]}, pd.date_range('1970-01-01', periods=3, freq='S')),
        pd.DataFrame({'a': [1.01, 2.02, 3.]}, pd.date_range('1970-01-01', periods=3, freq='S')),
        1e-2,   # tolerance
    ),
])
def test_df_compare_same_with_custom_float_precision(df1, df2, tolerance):
    assert_(df_compare(df1, df2, verbose=True, rtol=tolerance))


@pytest.mark.parametrize(('ts1', 'ts2', 'tolerance'), [
    (
        pd.TimeSeries([1., 2., 3.], pd.date_range('1970-01-01', periods=3, freq='S')),
        pd.TimeSeries([1.0001, 2.0002, 3.], pd.date_range('1970-01-01', periods=3, freq='S')),
        1e-4,   # tolerance
    ),
    (
        pd.TimeSeries([1., 2., 3.], pd.date_range('1970-01-01', periods=3, freq='S')),
        pd.TimeSeries([1.01, 2.02, 3.], pd.date_range('1970-01-01', periods=3, freq='S')),
        1e-2,   # tolerance
    ),
])
def test_ts_compare_same_with_custom_float_precision(ts1, ts2, tolerance):
    assert_(ts_compare(ts1, ts2, verbose=True, rtol=tolerance))

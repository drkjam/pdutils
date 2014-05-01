import datetime as dt

import pytest
import jsonpickle
import numpy as np
import pandas as pd

from pdutils.serialize.json import register_handlers
from pdutils.compare import ndarray_compare, ts_compare, df_compare
from pdutils.assert_funcs import assert_

register_handlers()


@pytest.mark.parametrize('arr', [
    np.array([1, 2, 3]),
    np.array([1., 2., 3.]),
    np.array(['foo', 'bar', 'baz']),
    np.array([dt.datetime(1970, 1, 1, 12, 57), dt.datetime(1970, 1, 1, 12, 58), dt.datetime(1970, 1, 1, 12, 59)]),
    np.array([dt.date(1970, 1, 1), dt.date(1970, 1, 2), dt.date(1970, 1, 3)]),
])
def test_numpy_array_handler(arr):
    buf = jsonpickle.encode(arr)
    arr_after = jsonpickle.decode(buf)
    assert_(ndarray_compare(arr, arr_after))


@pytest.mark.parametrize('ts', [
    pd.TimeSeries([1, 2, 3], index=[0, 1, 2]),
    pd.TimeSeries([1., 2., 3.], pd.date_range('1970-01-01', periods=3, freq='S'))
])
def test_pandas_timeseries_handler(ts):
    buf = jsonpickle.encode(ts)
    ts_after = jsonpickle.decode(buf)
    assert_(ts_compare(ts, ts_after))


@pytest.mark.parametrize('df', [
    pd.DataFrame({0: [1, 2, 3]}, index=[0, 1, 2]),
    pd.DataFrame({0: [1, 2, 3], 1: [1.1, 2.2, 3.3]}, index=[0, 1, 2]),
    pd.DataFrame({0: [1, 2, 3], 1: [1.1, 2.2, 3.3]}, index=pd.date_range('1970-01-01', periods=3, freq='S')),
])
def test_pandas_dataframe_handler(df):
    buf = jsonpickle.encode(df)
    ts_after = jsonpickle.decode(buf)
    assert_(df_compare(df, ts_after))


def test_mixed_python_and_pandas_types():
    data = (
        np.array([1., 2., 3.]),
        pd.TimeSeries([1, 2, 3], index=[0, 1, 2]),
        pd.DataFrame({0: [1, 2, 3], 1: [1.1, 2.2, 3.3]}, index=pd.date_range('1970-01-01', periods=3, freq='S'))
    )
    buf = jsonpickle.encode(data)
    data_after = jsonpickle.decode(buf)

    assert isinstance(data, tuple)
    assert len(data) == 3
    assert_(ndarray_compare(data[0], data_after[0]))
    assert_(ts_compare(data[1], data_after[1]))
    assert_(df_compare(data[2], data_after[2]))

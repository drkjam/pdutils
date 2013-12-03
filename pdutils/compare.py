"""Functions for comparing numpy arrays and pandas TimeSeries and DataFrame objects."""

import numpy as np


_strip_nans = lambda a: a[np.negative(np.isnan(a))]


def ndarray_compare(left, right, rtol=1.e-5, atol=1.e-8):
    """Compares two numpy.ndarray objects for equivalence.
    
    Parameters
    ----------
    left : numpy.ndarray
        array on the left hand side of the comparison.
    
    right : numpy.ndarray
        array on the right hand side of the comparison.
    
    rtol : float
        The relative tolerance parameter used for np.allclose() comparisons.

    atol : float
        The absolute tolerance parameter for np.allclose() comparisons.

    Returns
    -------
    equivalent, status : tuple
        If `equivalent` is True the numpy arrays are considered equal, if False
        they are not. `status` is an empty string if equivalent is True, or a
        string containing specific details of the comparison failure otherwise. 
    """
    if left.dtype != right.dtype:
        return False, 'dtype mismatch! left: %r, right: %r' % (left.dtype, right.dtype)

    if np.issubdtype(left.dtype, np.floating):
        if not np.all(np.isnan(left) == np.isnan(right)):
            return False, 'NaN value positions do not match!'
        if not np.allclose(_strip_nans(left), _strip_nans(right), rtol=rtol, atol=atol):
            return False, 'values are different!'
    else:
        if not np.all(left == right):
            return False, 'values are different!'

    return True, 'values are equivalent'


def ts_compare(left, right, rtol=1.e-5, atol=1.e-8, verbose=False):
    """Compares two pandas.TimeSeries objects for equivalence.

    Parameters
    ----------
    left : pandas.TimeSeries
        TimeSeries on the left hand side of the comparison.

    right : pandas.TimeSeries
        TimeSeries on the right hand side of the comparison.

    rtol : float
        The relative tolerance parameter used for np.allclose() comparisons. (optional)

    atol : float
        The absolute tolerance parameter for np.allclose() comparisons. (optional)

    verbose: bool
        If True displays detailed comparison information. (optional)
        Default: False

    Returns
    -------
    equivalent, status : tuple
        If `equivalent` is True the TimeSeries objects are considered equal, if
        False they are not. `status` is an empty string if equivalent is True,
        or a string containing specific details of the comparison failure
        otherwise.

    Notes
    -----
    For our purposes equivalent is defined as the TimeSeries objects with the
    following attributes :

    1. Both have the same number of rows

    2. Both have a data column with the same dtype

    3. Both have the same index type and values

    4. The position of NaN values are significant (applies to floating point
       dtypes only).

    5. both sides have column values are strictly equal (according to
       np.all(...)) for all data types apart from floating point (which
       are compared equal with a specified tolerance using np.allclose(...)).
    """
    if left.size != right.size:
        return False, 'row count mismatch!' \
            'left has %d value(s), right has %d value(s)' \
                % (left.size, right.size)

    if type(left.index) is not type(right.index):
        return False, 'index type mismatch!' \
            'left index type %s, right index type %s' \
                % (type(left.index), type(right.index))

    if not np.all(left.index.values == right.index.values):
        return False, 'index values are not the same!'

    equivalent, msg = ndarray_compare(left.values, right.values, rtol=rtol, atol=atol)
    if not equivalent:
        comparison_data = ''
        if verbose:
            comparison_data = '\nLEFT TimeSeries:\n%r\nRIGHT TimeSeries:\n%r\n' % (left, right)
        return False, 'comparison of values failed! %s%s' % (msg, comparison_data)

    return True, 'TimeSeries contents are equivalent'


def df_compare(left, right, rtol=1.e-5, atol=1.e-8, verbose=False):
    """Compares two pandas.DataFrame objects for equivalence.

    Parameters
    ----------
    left : pandas.DataFrame
        DataFrame on the left hand side of the comparison.

    right : pandas.DataFrame
        DataFrame on the right hand side of the comparison.
    
    rtol : float
        The relative tolerance parameter used for np.allclose() comparisons. (optional)

    atol : float
        The absolute tolerance parameter for np.allclose() comparisons. (optional)

     verbose: bool
        If True displays detailed comparison information. (optional)
        Default: False

   Returns
    -------
    equivalent, status : tuple
        If `equivalent` is True the DataFrame objects are considered equal, if
        False they are not. `status` is an empty string if equivalent is True,
        or a string containing specific details of the comparison failure
        otherwise. 

    Notes
    -----
    For our purposes equivalent is defined as the DataFrame objects with the
    following attributes :
    
    1. Both have the same number of rows
    
    2. Both have the same number of columns

    3. Both have the same combination of column names and dtypes
       (NB - the order in which the columns appears is *not*
       significant).

    4. Both have the same index type and values

    5. The position of NaN values is significant for columns that have a
       floating point dtype.

    6. both sides have column values are strictly equal (according to
       np.all(...)) for all data types apart from floating point (which
    are compared equal with a specified tolerance using np.allclose(...)).
    """
    if left.columns.size != right.columns.size:
        return False, 'column count mismatch!' \
            'left has %d column(s), right has %d column(s)' \
                % (left.columns.size, right.columns.size)

    if len(left) != len(right):
        return False, 'row count mismatch!' \
            'left has %d row(s), right has %d row(s)' \
                % (len(left), len(right))

    lcols = set(left.columns.values.tolist())
    rcols = set(right.columns.values.tolist())
    
    if lcols != rcols:
        return False, 'column name mismatch!\ncommon column name(s): %r\n' \
            'left-only column name(s): %r\nright-only column name(s) %r' \
                % (lcols & rcols, rcols ^ (lcols | rcols), lcols ^ (lcols | rcols))

    if type(left.index) is not type(right.index):
        return False, 'index type mismatch! left index type %s, right index type %s' \
            % (type(left.index), type(right.index))

    if not np.all(left.index.values == right.index.values):
        return False, 'index values are not the same!'

    for col in sorted(lcols):
        equivalent, msg = ndarray_compare(left[col].values, right[col].values, rtol=rtol, atol=atol)
        if not equivalent:
            comparison_data = ''
            if verbose:
                comparison_data = '\nLEFT DataFrame:\n%r\nRIGHT DataFrame:\n%r\n' \
                    % (left[sorted(left.columns)], right[sorted(right.columns)])
            return False, 'comparison of column %r failed! %s%s' % (col, msg, comparison_data)

    return True, 'DataFrame contents are equivalent'


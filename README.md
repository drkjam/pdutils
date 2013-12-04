pdutils - pandas utilities 
==========================

Introduction
------------

The intention of this package is simple - to make testing with pandas easy.

Here's an example of the intended API usage :

    from pdutils import ts_compare, assert_

    ...

    def test1():
        # initialise two pandas TimeSeries objects for comparison, then ...
        assert_(ts_compare(ts1, ts2))

The test should pass if both TimeSeries objects are equivalent.

If the comparison fails, by default, the assertion should provide a terse, yet meaningful message
about the difference that cause the assertion failure.

A more details comparison can be extracted using the verbose option.

    def test2():
        # initialise two pandas TimeSeries objects for comparison, then ...
        assert_(ts_compare(ts1, ts2, verbose=True))

This should provide an over and under view of the difference found in a particular column, where applicable.

For columns containing float types it is also possible to configure the tolerance of the
comparison (see docstrings for further details).

API
---

Function exist to allow you to compare pandas TimeSeries, DataFrames and numpy arrays.

    ts_compare(x, y)

Compares two pandas.TimeSeries object for equivalence.

    df_compare(x, y)

Compares two pandas.DataFrame objects for equivalence.

    ndarray_compare(x, y)

Compares two numpy arrays for equivalence.

    assert_((expr, failure_msg))

Like the Python assert statement but in functional form.

    assert_not((expr, failure_msg))

A negative assertion in functional form.

TODO
----
In no particular order, these are the things that should be changed / added in future.

* add comparison support for Panels
* more details comparison of multi-dimensional numpy arrays

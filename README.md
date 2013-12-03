pdutils - pandas utilities 
==========================

Introduction
------------

The intention of this package is simple - to make testing with pandas painless and simple.

To use the API effectively, the intentino is to write tests that look something like this :

    from pdutils import ts_compare, assert_

    ...

    def test_x():
        # initialise two pandas TimeSeries objects for comparison, then ...
        assert_(ts_compare(ts1, ts2)

The test should pass if both TimeSeries objects compare favourably.

If they fail, the assertion should provide a meaningful message about what is different between the objects being compared.


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
* some form of diff view comparing both sides (currently this is a very simple message).

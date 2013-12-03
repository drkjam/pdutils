import pytest

from pdutils import assert_, assert_not


def test_assert_():
    assert_((True, ''))

    with pytest.raises(AssertionError):
        assert_((False, ''))


def test_assert_not():
    assert_not((False, ''))

    with pytest.raises(AssertionError):
        assert_not((True, ''))

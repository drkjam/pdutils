"""Assertion functions that wrap Python's assert statement."""

def assert_(args):
    """Provides a functional equivalent of the Python assert statement."""
    assert isinstance(args[0], bool)
    assert isinstance(args[1], str)
    assert args[0], args[1]


def assert_not(args):
    """Provides a functional negative assertion callable for Python's assert statement."""
    assert isinstance(args[0], bool)
    assert isinstance(args[1], str)
    assert not args[0], args[1]



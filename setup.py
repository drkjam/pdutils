import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

class PyTest(TestCommand):
    user_options = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

setup(
    name="pdutils",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'numpy>=1.7.1',
        'pandas>=0.10.1',
    ],
    tests_require=['pytest>=2.4.2'],
    author="David Moss",
    author_email="drkjam@gmail.com",
    description="Utilities for the pandas library",
    license="MIT",
    keywords="pandas",
    url="http://github.com/drkjam/pdutils",
    cmdclass={'test': PyTest},
)

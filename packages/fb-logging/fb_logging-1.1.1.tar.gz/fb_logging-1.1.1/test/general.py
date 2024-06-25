#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@summary: General used functions an objects used for unit tests on the logging python modules.

@author: Frank Brehm
@contact: frank@brehm-online.com
@copyright: © 2024 Frank Brehm, Berlin
@license: AGPL
"""

import argparse
import logging
import os
import pprint
import sys
from logging import Formatter
try:
    import unittest2 as unittest
except ImportError:
    import unittest


# =============================================================================

LOG = logging.getLogger(__name__)


# =============================================================================
def get_arg_verbose():
    """Get and return command line arguments."""
    arg_parser = argparse.ArgumentParser()

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        '-v', '--verbose', action='count',
        dest='verbose', help='Increase the verbosity level')
    args = arg_parser.parse_args()

    return args.verbose


# =============================================================================
def init_root_logger(verbose=0):
    """Initialize the root logger."""
    root_log = logging.getLogger()
    root_log.setLevel(logging.WARNING)
    if verbose:
        root_log.setLevel(logging.INFO)
        if verbose > 1:
            root_log.setLevel(logging.DEBUG)

    appname = os.path.basename(sys.argv[0])
    format_str = appname + ': '
    if verbose:
        if verbose > 1:
            format_str += '%(name)s(%(lineno)d) %(funcName)s() '
        else:
            format_str += '%(name)s '
    format_str += '%(levelname)s - %(message)s'
    formatter = None
    formatter = Formatter(format_str)

    # create log handler for console output
    lh_console = logging.StreamHandler(sys.stderr)
    if verbose:
        lh_console.setLevel(logging.DEBUG)
    else:
        lh_console.setLevel(logging.INFO)
    lh_console.setFormatter(formatter)

    root_log.addHandler(lh_console)


# =============================================================================
def pp(value, indent=4, width=99, depth=None):
    """
    Return a pretty print string of the given value.

    @return: pretty print string
    @rtype: str
    """
    pretty_printer = pprint.PrettyPrinter(
        indent=indent, width=width, depth=depth)
    return pretty_printer.pformat(value)


# =============================================================================
class FbLoggingTestcase(unittest.TestCase):
    """Base test case for all testcase classes of this package."""

    # -------------------------------------------------------------------------
    def __init__(self, methodName='runTest', verbose=0):
        """Initialize the base testcase class."""
        self._verbose = int(verbose)

        appname = os.path.basename(sys.argv[0]).replace('.py', '')
        self._appname = appname

        super(FbLoggingTestcase, self).__init__(methodName)

        self.assertGreaterEqual(
            sys.version_info[0], 3, 'Unsupported Python version {}.'.format(sys.version))

        if sys.version_info[0] == 3:
            self.assertGreaterEqual(
                sys.version_info[1], 6, 'Unsupported Python version {}.'.format(sys.version))

        if self.verbose >= 3:
            LOG.debug('Used Phyton version: {!r}.'.format(sys.version))

    # -------------------------------------------------------------------------
    @property
    def verbose(self):
        """Return the verbosity level."""
        return getattr(self, '_verbose', 0)

    # -------------------------------------------------------------------------
    @property
    def appname(self):
        """Return the name of the current running application."""
        return self._appname

    # -------------------------------------------------------------------------
    def setUp(self):
        """Execute this on seting up before calling each particular test method."""
        pass

    # -------------------------------------------------------------------------
    def tearDown(self):
        """Tear down routine for calling each particular test method."""
        pass


# =============================================================================
if __name__ == '__main__':

    pass

# =============================================================================

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

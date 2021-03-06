#!/usr/bin/env python

import optparse
import sys
import unittest

from walrus import tests

def runtests(verbose=False, failfast=False, names=None):
    if names:
        suite = unittest.TestLoader().loadTestsFromNames(names, tests)
    else:
        suite = unittest.TestLoader().loadTestsFromModule(tests)
    runner = unittest.TextTestRunner(verbosity=2 if verbose else 1,
                                     failfast=failfast)
    return runner.run(suite)

if __name__ == '__main__':
    try:
        from redis import Redis
    except ImportError:
        raise RuntimeError('redis-py must be installed.')
    else:
        try:
            Redis().info()
        except:
            raise RuntimeError('redis server does not appear to be running')

    parser = optparse.OptionParser()
    parser.add_option('-v', '--verbose', action='store_true', default=False,
                      dest='verbose', help='Verbose output.')
    parser.add_option('-f', '--failfast', action='store_true', default=False,
                      help='Stop on first failure or error.')
    options, args = parser.parse_args()
    result = runtests(
        verbose=options.verbose,
        failfast=options.failfast,
        names=args)

    if result.failures:
        sys.exit(1)
    elif result.errors:
        sys.exit(2)

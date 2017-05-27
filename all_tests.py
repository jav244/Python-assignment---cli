from unit_tests import *
from more_unit_tests import *

import unittest


def my_suite():
    theSuite = unittest.TestSuite()
    theSuite.addTest(unittest.makeSuite(MainTests))
    theSuite.addTest(unittest.makeSuite(ConTests))

    return theSuite

if __name__ == "__main__":  # pragma: no cover
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = my_suite()
    runner.run(test_suite)

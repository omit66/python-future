# Test code for fix_xrange_with_six_import.py

# Python imports
from lib2to3 import fixer_util
from fixertestcase import FixerTestCase


class Test_xrange(FixerTestCase):
    fixer = "xrange_with_six"

    def test_prefix_preservation(self):
        b = """x =    xrange(  10  )"""
        a = """from six.moves import xrange\nx =    xrange(  10  )"""
        self.check(b, a)

        b = """x = xrange(  1  ,  10   )"""
        a = """from six.moves import xrange\nx = xrange(  1  ,  10   )"""
        self.check(b, a)

        b = """x = xrange(  0  ,  10 ,  2 )"""
        a = """from six.moves import xrange\nx = xrange(  0  ,  10 ,  2 )"""
        self.check(b, a)

    def test_single_arg(self):
        b = """x = xrange(10)"""
        a = """from six.moves import xrange\nx = xrange(10)"""
        self.check(b, a)

    def test_two_args(self):
        b = """x = xrange(1, 10)"""
        a = """from six.moves import xrange\nx = xrange(1, 10)"""
        self.check(b, a)

    def test_three_args(self):
        b = """x = xrange(0, 10, 2)"""
        a = """from six.moves import xrange\nx = xrange(0, 10, 2)"""
        self.check(b, a)

    def test_range_unchange(self):
        a = """x = range(10, 3, 9)"""
        self.unchanged(a)

    def test_xrange_in_for(self):
        b = """for i in xrange(10):\n    j=i"""
        a = """from six.moves import xrange\nfor i in xrange(10):\n    j=i"""
        self.check(b, a)

        b = """[i for i in xrange(10)]"""
        a = """from six.moves import xrange\n[i for i in xrange(10)]"""
        self.check(b, a)

    def test_range_in_for_unchanged(self):
        self.unchanged("for i in range(10): pass")
        self.unchanged("[i for i in range(10)]")

    def test_in_consuming_context(self):
        for call in fixer_util.consuming_calls:
            a = "a = %s(xrange(10))" % call
            b = "from six.moves import xrange\na = %s(xrange(10))" % call
            self.check(a, b)

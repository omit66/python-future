# Test code for fix_xrange_with_six_import.py

# Python imports
from lib2to3 import fixer_util
from fixertestcase import FixerTestCase


class Test_xrange(FixerTestCase):
    fixer = "xrange"

    def test_prefix_preservation(self):
        b = """x =    xrange(  10  )"""
        a = """import six.moves\nx =    six.moves.xrange(  10  )"""
        self.check(b, a)

        b = """x = xrange(  1  ,  10   )"""
        a = """import six.moves\nx = six.moves.xrange(  1  ,  10   )"""
        self.check(b, a)

        b = """x = xrange(  0  ,  10 ,  2 )"""
        a = """import six.moves\nx = six.moves.xrange(  0  ,  10 ,  2 )"""
        self.check(b, a)

    def test_single_arg(self):
        b = """x = xrange(10)"""
        a = """import six.moves\nx = six.moves.xrange(10)"""
        self.check(b, a)

    def test_two_args(self):
        b = """x = xrange(1, 10)"""
        a = """import six.moves\nx = six.moves.xrange(1, 10)"""
        self.check(b, a)

    def test_three_args(self):
        b = """x = xrange(0, 10, 2)"""
        a = """import six.moves\nx = six.moves.xrange(0, 10, 2)"""
        self.check(b, a)

    def test_range(self):
        a = """x = range(10, 3, 9)"""
        b = """import past.builtins\nx = past.builtins.range(10, 3, 9)"""
        self.check(a, b)

    def test_xrange_in_for(self):
        a = """for i in xrange(10):\n    j=i"""
        b = """import six.moves\nfor i in six.moves.xrange(10):\n    j=i"""
        self.check(a, b)

        a = """[i for i in xrange(10)]"""
        b = """import six.moves\n[i for i in six.moves.xrange(10)]"""
        self.check(a, b)

    def test_range_in_for(self):
        a = "for i in range(10): pass"
        b = "import past.builtins\nfor i in past.builtins.range(10): pass"
        self.check(a, b)
        c = "[i for i in range(10)]"
        d = "import past.builtins\n[i for i in past.builtins.range(10)]"
        self.check(c, d)

    def test_in_consuming_context(self):
        for call in fixer_util.consuming_calls:
            a = "a = %s(xrange(10))" % call
            b = "import six.moves\na = %s(six.moves.xrange(10))" % call
            self.check(a, b)

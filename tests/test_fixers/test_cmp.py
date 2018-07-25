from fixertestcase import FixerTestCase


class Test_cmp(FixerTestCase):
    fixer = "cmp_inline"

    def test_cmp(self):
        b = """cmp(a, b)"""
        a = """(a > b) - (a < b)"""
        self.check(b, a)

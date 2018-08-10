from fixertestcase import FixerTestCase


class Test_unichr(FixerTestCase):
    fixer = "unichr"

    def test_unichr(self):
        b = """unichr(42)"""
        a = """import six.moves\nsix.moves.unichr(42)"""
        self.check(b, a)

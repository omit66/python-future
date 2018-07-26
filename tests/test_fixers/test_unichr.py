from fixertestcase import FixerTestCase


class Test_zip(FixerTestCase):
    fixer = "unichr"

    def test_unichr(self):
        b = """unichr(42)"""
        a = """import six\nsix.unichr(42)"""
        self.check(b, a)

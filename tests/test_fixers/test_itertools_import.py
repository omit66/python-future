from fixertestcase import FixerTestCase


class Test_itertools_imports(FixerTestCase):
    fixer = "itertools_imports"

    def test_reduced(self):
        b = "from itertools import imap, izip, foo"
        a = "import six.moves\nfrom itertools import foo"
        self.check(b, a)

        b = "from itertools import bar, imap, izip, foo"
        a = "import six.moves\nfrom itertools import bar, foo"
        self.check(b, a)

        b = "from itertools import chain, imap, izip"
        a = "import six.moves\nfrom itertools import chain"
        self.check(b, a)

    def test_comments(self):
        b = "#foo\nfrom itertools import imap, izip"
        a = "#foo\nimport six.moves\n"
        self.check(b, a)

    def test_none(self):
        b = "from itertools import imap, izip"
        a = "import six.moves\n"
        self.check(b, a)

        b = "from itertools import izip"
        a = "import six.moves\n"
        self.check(b, a)

    def test_import_as(self):
        b = "from itertools import izip, bar as bang, imap"
        a = "import six.moves\nfrom itertools import bar as bang"
        self.check(b, a)

        b = "from itertools import izip as _zip, imap, bar"
        a = "import six.moves\nfrom six.moves import zip as _zip\n"\
            "from itertools import bar"
        self.check(b, a)

        b = "from itertools import imap as _map"
        a = "from six.moves import map as _map\n"
        self.check(b, a)

        b = "from itertools import imap as _map, izip as _zip"
        a = "from six.moves import zip as _zip\n"\
            "from six.moves import map as _map\n"
        self.check(b, a)

        s = "from itertools import bar as bang"
        self.unchanged(s)

    def test_ifilter_and_zip_longest(self):
        for name in "filterfalse", "zip_longest":
            b = "from itertools import i%s" % (name,)
            a = "import six.moves\n"
            self.check(b, a)

            b = "from itertools import imap, i%s, foo" % (name,)
            a = "import six.moves\nfrom itertools import foo"
            self.check(b, a)

            b = "from itertools import bar, i%s, foo" % (name,)
            a = "import six.moves\nfrom itertools import bar, foo"
            self.check(b, a)

    def test_import_star(self):
        s = "from itertools import *"
        self.unchanged(s)

    def test_unchanged(self):
        s = "from itertools import foo"
        self.unchanged(s)

    def test_izip(self):
        # fixer_tools will replace izip(...)
        b = "from itertools import izip\nizip([1, 2], [1])"""
        a = "import six.moves\n\nizip([1, 2], [1])"
        self.check(b, a)

    def test_imap(self):
        # fixer_tools will replace imap(...)
        s = """import itertools\nitertools.imap(lambda x: x * 2, [1, 2])"""
        self.unchanged(s)

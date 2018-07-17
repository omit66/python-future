# Test code for fix_dict.py

# Python imports
from lib2to3 import fixer_util
from fixertestcase import FixerTestCase


class Test_dict(FixerTestCase):
    fixer = "dict"

    def test_prefix_preservation(self):
        b = "if   d. keys  (  )  : pass"
        a = "if   list(d)  : pass"
        self.check(b, a)

        b = "if   d. items  (  )  : pass"
        a = "from future.utils import listitems\nif   listitems(d)  : pass"
        self.check(b, a)

        b = "if   d. iterkeys  ( )  : pass"
        a = "from six import iterkeys\nif   iterkeys(d)  : pass"
        self.check(b, a)

        b = "[i for i in    d.  iterkeys(  )  ]"
        a = "from six import iterkeys\n[i for i in    iterkeys(d)  ]"
        self.check(b, a)

        b = "if   d. viewkeys  ( )  : pass"
        a = "from six import viewkeys\nif   viewkeys(d)  : pass"
        self.check(b, a)

        b = "[i for i in    d.  viewkeys(  )  ]"
        a = "from six import viewkeys\n[i for i in    viewkeys(d)  ]"
        self.check(b, a)

    def test_trailing_comment(self):
        b = "d.keys() # foo"
        a = "list(d) # foo"
        self.check(b, a)

        b = "d.items()  # foo"
        a = "from future.utils import listitems\nlistitems(d)  # foo"
        self.check(b, a)

        b = "d.iterkeys()  # foo"
        a = "from six import iterkeys\niterkeys(d)  # foo"
        self.check(b, a)

        b = """[i for i in d.iterkeys() # foo
               ]"""
        a = """from six import iterkeys\n[i for i in iterkeys(d) # foo
               ]"""
        self.check(b, a)

        b = """[i for i in d.iterkeys() # foo
               ]"""
        a = """from six import iterkeys\n[i for i in iterkeys(d) # foo
               ]"""
        self.check(b, a)

        b = "d.viewitems()  # foo"
        a = "from six import viewitems\nviewitems(d)  # foo"
        self.check(b, a)

    def test_unchanged(self):
        for wrapper in fixer_util.consuming_calls:
            s = "s = %s(d.keys())" % wrapper
            self.unchanged(s)

            s = "s = %s(d.values())" % wrapper
            self.unchanged(s)

            s = "s = %s(d.items())" % wrapper
            self.unchanged(s)

    def test_01(self):
        b = "d.keys()"
        a = "list(d)"
        self.check(b, a)

        b = "a[0].foo().keys()"
        a = "list(a[0].foo())"
        self.check(b, a)

    def test_02(self):
        b = "d.items()"
        a = "from future.utils import listitems\nlistitems(d)"
        self.check(b, a)

    def test_03(self):
        b = "d.values()"
        a = "from future.utils import listvalues\nlistvalues(d)"
        self.check(b, a)

    def test_04(self):
        b = "d.iterkeys()"
        a = "from six import iterkeys\niterkeys(d)"
        self.check(b, a)

    def test_05(self):
        b = "d.iteritems()"
        a = "from six import iteritems\niteritems(d)"
        self.check(b, a)

    def test_06(self):
        b = "d.itervalues()"
        a = "from six import itervalues\nitervalues(d)"
        self.check(b, a)

    def test_07(self):
        s = "list(d.keys())"
        self.unchanged(s)

    def test_08(self):
        s = "sorted(d.keys())"
        self.unchanged(s)

    def test_09(self):
        b = "iter(d.keys())"
        a = "iter(list(d))"
        self.check(b, a)

    def test_10(self):
        b = "foo(d.keys())"
        a = "foo(list(d))"
        self.check(b, a)

    def test_11(self):
        b = "for i in d.keys(): print i"
        a = "for i in list(d): print i"
        self.check(b, a)

    def test_12(self):
        b = "for i in d.iterkeys(): print i"
        a = "from six import iterkeys\nfor i in iterkeys(d): print i"
        self.check(b, a)

    def test_13(self):
        b = "[i for i in d.keys()]"
        a = "[i for i in list(d)]"
        self.check(b, a)

    def test_14(self):
        b = "[i for i in d.iterkeys()]"
        a = "from six import iterkeys\n[i for i in iterkeys(d)]"
        self.check(b, a)

    def test_15(self):
        b = "(i for i in d.keys())"
        a = "(i for i in list(d))"
        self.check(b, a)

    def test_16(self):
        b = "(i for i in d.iterkeys())"
        a = "from six import iterkeys\n(i for i in iterkeys(d))"
        self.check(b, a)

    def test_17(self):
        b = "iter(d.iterkeys())"
        a = "from six import iterkeys\niter(iterkeys(d))"
        self.check(b, a)

    def test_18(self):
        b = "list(d.iterkeys())"
        a = "from six import iterkeys\nlist(iterkeys(d))"
        self.check(b, a)

    def test_19(self):
        b = "sorted(d.iterkeys())"
        a = "from six import iterkeys\nsorted(iterkeys(d))"
        self.check(b, a)

    def test_20(self):
        b = "foo(d.iterkeys())"
        a = "from six import iterkeys\nfoo(iterkeys(d))"
        self.check(b, a)

    def test_21(self):
        b = "print h.iterkeys().next()"
        a = "from six import iterkeys\nprint iterkeys(h).next()"
        self.check(b, a)

    def test_22(self):
        b = "print h.keys()[0]"
        a = "print list(h)[0]"
        self.check(b, a)

    def test_23(self):
        b = "print list(h.iterkeys().next())"
        a = "from six import iterkeys\nprint list(iterkeys(h).next())"
        self.check(b, a)

    def test_24(self):
        b = "for x in h.keys()[0]: print x"
        a = "for x in list(h)[0]: print x"
        self.check(b, a)

    def test_25(self):
        b = "d.viewkeys()"
        a = "from six import viewkeys\nviewkeys(d)"
        self.check(b, a)

    def test_26(self):
        b = "d.viewitems()"
        a = "from six import viewitems\nviewitems(d)"
        self.check(b, a)

    def test_27(self):
        b = "d.viewvalues()"
        a = "from six import viewvalues\nviewvalues(d)"
        self.check(b, a)

    def test_28(self):
        b = "[i for i in d.viewkeys()]"
        a = "from six import viewkeys\n[i for i in viewkeys(d)]"
        self.check(b, a)

    def test_29(self):
        b = "(i for i in d.viewkeys())"
        a = "from six import viewkeys\n(i for i in viewkeys(d))"
        self.check(b, a)

    def test_30(self):
        b = "iter(d.viewkeys())"
        a = "from six import viewkeys\niter(viewkeys(d))"
        self.check(b, a)

    def test_31(self):
        b = "list(d.viewkeys())"
        a = "from six import viewkeys\nlist(viewkeys(d))"
        self.check(b, a)

    def test_32(self):
        b = "sorted(d.viewkeys())"
        a = "from six import viewkeys\nsorted(viewkeys(d))"
        self.check(b, a)

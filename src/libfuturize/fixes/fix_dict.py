# Copyright 2007 Google, Inc. All Rights Reserved.
# Licensed to PSF under a Contributor Agreement.

"""Fixer for dict methods.

d.keys() -> list(d)
d.items() -> from future.utils import listitems\nlistitems(d)
d.values() -> from future.utils import listvalues\nlistvalues(d)

d.iterkeys() -> from six import iterkeys\niterkeys(d)
d.iteritems() -> from six import iteritems\niteritems(d)
d.itervalues() -> from six import itervalues\nitervalues(d)

d.viewkeys() -> from six import viewkeys\nviewkeys(d)
d.viewitems() -> from six import viewitems\nviewitems(d)
d.viewvalues() -> from six import viewvalues\nviewvalues(d)

Except in certain very specific contexts: the iter() can be dropped
when the context is list(), sorted(), iter() or for...in; the list()
can be dropped when the context is list() or sorted() (but not iter()
or for...in!). Special contexts that apply to both: list(), sorted(), tuple()
set(), any(), all(), sum().
"""

# Local imports
from lib2to3 import patcomp, pytree, fixer_base
from lib2to3.fixer_util import Name, Call, Dot
from lib2to3 import fixer_util
from libfuturize.fixer_util import touch_import_top


iter_exempt = fixer_util.consuming_calls | set(["iter"])


class FixDict(fixer_base.BaseFix):
    BM_compatible = True

    PATTERN = """
    power< head=any+
         trailer< '.' method=('keys'|'items'|'values'|
                              'iterkeys'|'iteritems'|'itervalues'|
                              'viewkeys'|'viewitems'|'viewvalues') >
         parens=trailer< '(' ')' >
         tail=any*
    >
    """

    def transform(self, node, results):
        head = results["head"]
        method = results["method"][0]  # Extract node for method name
        tail = results["tail"]
        syms = self.syms
        method_name = method.value
        isiter = method_name.startswith(u"iter")
        isview = method_name.startswith(u"view")
        head = [n.clone() for n in head]
        tail = [n.clone() for n in tail]
        # no changes neccessary if the call is in a special context
        special = not tail and self.in_special_context(node, isiter)
        new = pytree.Node(syms.power, head)
        new.prefix = u""
        if isiter or isview:
            # replace the method with the six function
            # e.g. d.iteritems() -> from six import iteritems\n iteritems(d)
            new = Call(Name(method_name), [new])
            touch_import_top('six', method_name, node)
        elif special:
            # it is not neccessary to change this case
            return node
        elif method_name in ("items", "values"):
            # ensure to return a list in python 3
            new = Call(Name(u"list" + method_name), [new])
            touch_import_top('future.utils', 'list' + method_name,
                                        node)
        else:
            # method_name is "keys"; removed it and cast the dict to list
            new = Call(Name(u"list"), [new])

        if tail:
            new = pytree.Node(syms.power, [new] + tail)
        new.prefix = node.prefix
        return new

    P1 = "power< func=NAME trailer< '(' node=any ')' > any* >"
    p1 = patcomp.compile_pattern(P1)

    def in_special_context(self, node, isiter):
        # it is not wrapped
        if node.parent is None:
            return False
        results = {}
        if (node.parent.parent is not None and
           self.p1.match(node.parent.parent, results) and
           results["node"] is node):

            if isiter:
                # iter(d.iterkeys()) -> iter(d.keys()), etc.
                return results["func"].value in iter_exempt
            else:
                # list(d.keys()) -> list(d.keys()), etc.
                return results["func"].value in fixer_util.consuming_calls
        return False

# Copyright 2007 Google, Inc. All Rights Reserved.
# Licensed to PSF under a Contributor Agreement.

"""Fixer that changes xrange(...) into from six import xrange\nxrange(...).
It is easier to use six instead of future, because we do not want to replace
the python2 range with the xrange behavior.
"""

# Local imports
from lib2to3 import fixer_base
from lib2to3.fixer_util import Name
from libfuturize.fixer_util import touch_import_top


class FixXrange(fixer_base.BaseFix):
    BM_compatible = True
    PATTERN = """
              power<
                 (name='range' | name='xrange') trailer< '(' args=any ')' >
              rest=any* >
              """

    def transform(self, node, results):
        name = results["name"]
        if name.value == u"xrange":
            touch_import_top(None, "six.moves", node)
            name.replace(Name(u"six.moves.xrange",  name.prefix))

        elif name.value == u'range':
            # range in PY2 and list(range) in PY3
            touch_import_top(None, 'past.builtins', node)
            name.replace(Name(u"past.builtins.range", name.prefix))

        else:
            raise ValueError(repr(name))
        return node

""" This fix replaces the chr with six.int2bytes.
Which is chr(i) in Python2 and bytes((i,)) in Python3
"""
from lib2to3 import fixer_base
from lib2to3.fixer_util import is_probably_builtin, Name

from libfuturize.fixer_util import touch_import_top


class FixChr(fixer_base.BaseFix):
    BM_compatible = True

    PATTERN = """'chr'"""

    def transform(self, node, results):
        if is_probably_builtin(node):
            touch_import_top(None, u'six', node)
            node.replace(Name(u'six.int2byte', node.prefix))

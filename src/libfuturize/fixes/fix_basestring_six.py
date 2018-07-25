"""
Fixer replaces basestring -> six.string_types
and add 'import six'
"""

from lib2to3 import fixer_base
from lib2to3.fixer_util import Name

from libfuturize.fixer_util import touch_import_top


class FixBasestringSix(fixer_base.BaseFix):
    BM_compatible = True

    PATTERN = "'basestring'"

    def transform(self, node, results):
        touch_import_top(None, u'six', node)
        return Name(u'six.string_types', node.prefix)

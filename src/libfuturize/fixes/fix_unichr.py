from lib2to3 import fixer_base
from lib2to3.fixer_util import is_probably_builtin, Name

from libfuturize.fixer_util import touch_import_top


class FixUnichr(fixer_base.ConditionalFix):
    BM_compatible = True

    skip_on = 'six.moves.unichr'
    PATTERN = """'unichr'"""

    def transform(self, node, results):
        if self.should_skip(node):
            return
        if is_probably_builtin(node):
            touch_import_top(None, u'six', node)
            node.replace(Name(u'six.unichr', node.prefix))

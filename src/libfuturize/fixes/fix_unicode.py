from lib2to3 import fixer_base
from lib2to3.fixer_util import Name
from libfuturize.fixer_util import touch_import_top


class FixUnicode(fixer_base.BaseFix):
    BM_compatible = True
    PATTERN = """'unicode'"""

    def transform(self, node, results):
        touch_import_top(None, u'six', node)
        return Name(u'six.text_type', prefix=node.prefix)

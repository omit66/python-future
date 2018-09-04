from lib2to3 import fixer_base
from lib2to3 import pytree
from lib2to3.pgen2 import token

from libfuturize.fixer_util import future_import


class FixClassicDivision(fixer_base.BaseFix):
    _accept_type = token.SLASH

    def start_tree(self, tree, name):
        super(FixClassicDivision, self).start_tree(tree, name)
        self.skip = "division" in tree.future_features

    def match(self, node):
        return node.value == "/"

    def transform(self, node, results):
        if self.skip:
            return
        future_import(u'division', node)
        return pytree.Leaf(token.SLASH, "//", prefix=node.prefix)

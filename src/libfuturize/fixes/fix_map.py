# Copyright 2007 Google, Inc. All Rights Reserved.
# Licensed to PSF under a Contributor Agreement.

"""Fixer that changes map(F, ...) into past.builtins.map(F, ...) unless there
exists a 'from future_builtins import map' statement in the top-level
namespace.

As a special case, map(None, X) is changed into list(X).  (This is
necessary because the semantics are changed in this case -- the new
map(None, X) is equivalent to [(x,) for x in X].)

We avoid the transformation (except for the special case mentioned
above) if the map() call is directly contained in iter(<>), list(<>),
tuple(<>), sorted(<>), ...join(<>), or for V in <>:.

NOTE: This is still not correct if the original code was depending on
map(F, X, Y, ...) to go on until the longest argument is exhausted,
substituting None for missing values -- like zip(), it now stops as
soon as the shortest argument is exhausted.
"""

# Local imports
from lib2to3.pgen2 import token
from lib2to3 import fixer_base
from lib2to3.fixer_util import Name, Call, ListComp, in_special_context
from lib2to3.pygram import python_symbols as syms
from libfuturize.fixer_util import touch_import_top


class FixMap(fixer_base.ConditionalFix):
    BM_compatible = True

    PATTERN = """
    map_none=power<
        name='map'
        trailer< '(' arglist< 'None' ',' arg=any [','] > ')' >
    >
    |
    map_lambda=power<
        name='map'
        trailer<
            '('
            arglist<
                lambdef< 'lambda'
                         (fp=NAME | vfpdef< '(' fp=NAME ')'> ) ':' xp=any
                >
                ','
                it=any
            >
            ')'
        >
    >
    |
    power<
        name='map' trailer< '(' [arglist=any] ')' >
    >
    """

    skip_on = 'future_builtins.map'

    def transform(self, node, results):
        if self.should_skip(node):
            return

        name = results["name"]
        if node.parent.type == syms.simple_stmt:
            self.warning(node, "You should use a for loop here")
            name.replace(Name(u"six.moves.map", name.prefix))
            touch_import_top(None, u"six.moves", node)
            new = node.clone()
            new.prefix = u""
            new = Call(Name(u"list"), [new])
        elif "map_lambda" in results:
            new = ListComp(results["xp"].clone(),
                           results["fp"].clone(),
                           results["it"].clone())
        else:
            if "map_none" in results:
                new = results["arg"].clone()
            else:
                if "arglist" in results:
                    args = results["arglist"]
                    if args.type == syms.arglist and \
                       args.children[0].type == token.NAME and \
                       args.children[0].value == "None":
                        self.warning(node, "cannot convert map(None, ...) "
                                     "with multiple arguments because map() "
                                     "now truncates to the shortest sequence")
                        return
                if in_special_context(node):
                    return None
                name.replace(Name(u"six.moves.map", name.prefix))
                touch_import_top(None, u"six.moves", node)
                new = node.clone()
            new.prefix = u""
            new = Call(Name(u"list"), [new])
        new.prefix = node.prefix
        return new

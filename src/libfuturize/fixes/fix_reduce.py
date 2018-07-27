# Copyright 2008 Armin Ronacher.
# Licensed to PSF under a Contributor Agreement.
# Extended by CONTACT Software GmbH

"""Fixer for reduce().

reduce() -> six.reduce()
"""

from lib2to3 import fixer_base
from libfuturize.fixer_util import touch_import_top, Name


class FixReduce(fixer_base.BaseFix):

    BM_compatible = True
    order = "pre"

    PATTERN = """
    power< name='reduce'
        trailer< '('
            arglist< (
                (not(argument<any '=' any>) any ','
                 not(argument<any '=' any>) any) |
                (not(argument<any '=' any>) any ','
                 not(argument<any '=' any>) any ','
                 not(argument<any '=' any>) any)
            ) >
        ')' >
    >
    """

    def transform(self, node, results):
        name  = results['name']
        name.replace(Name(u'six.reduce', name.prefix))
        touch_import_top(None, u'six', node)

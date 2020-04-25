#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2020, Quantum Espresso Foundation and SISSA.
# Internazionale Superiore di Studi Avanzati). All rights reserved.
# This file is distributed under the terms of the BSD 3-Clause license.
# See the file 'LICENSE' in the root directory of the present distribution,
# or https://opensource.org/licenses/BSD-3-Clause
#
import os
import sys
import argparse
from functools import wraps

if not locals()['__package__']:
    # When this module is loaded before the package then __package__ is None or ''
    # and the relative imports are disabled. In this case import the package and
    # set __package__.
    #
    # $ python postqe --> __package__ == ''
    # $ python postqe/__main__.py --> __package__ is None
    #
    # Ref: https://www.python.org/dev/peps/pep-0366/ for details.
    sys.path[0] = ''
    pkg_search_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if pkg_search_path not in sys.path:
        sys.path.append(pkg_search_path)
    import xmlschema_codegen
    __package__ = xmlschema_codegen.__name__
else:
    import xmlschema_codegen as xg


PACKAGE_PATH = os.path.dirname(__file__)


def version_checked(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if sys.version_info < (3, 5, 0):
            sys.stderr.write("You need python 3.5 or later to run this program\n")
            sys.exit(1)
        func(*args, **kwargs)
    return wrapper



@version_checked
def main():
    parser = argparse.ArgumentParser(prog=__package__, add_help=True,
                                     description="Code generator for XSD schemas.")
    parser.usage = """%(prog)s 
    Try '%(prog)s --help' for more information."""
    args = parser.parse_args()
    xg.generate(args)


if __name__ == '__main__':
    main()
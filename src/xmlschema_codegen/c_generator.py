#
# Copyright (c) 2020, Quantum Espresso Foundation and SISSA.
# Internazionale Superiore di Studi Avanzati). All rights reserved.
# This file is distributed under the terms of the BSD 3-Clause license.
# See the file 'LICENSE' in the root directory of the present distribution,
# or https://opensource.org/licenses/BSD-3-Clause
#
from .base import filter_method, AbstractGenerator


class CGenerator(AbstractGenerator):
    """A C code generator for XSD schemas."""
    default_paths = ['templates/c/']

    builtin_types = {
        'string': 'str',
        'boolean': 'bool',
        'float': 'float',
        'double': 'double',
        'integer': 'int',
        'unsignedByte': 'unsigned short',
        'nonNegativeInteger': 'unsigned int',
        'positiveInteger': 'unsigned int',
    }

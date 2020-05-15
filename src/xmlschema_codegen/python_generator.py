#
# Copyright (c) 2020, Quantum Espresso Foundation and SISSA.
# Internazionale Superiore di Studi Avanzati). All rights reserved.
# This file is distributed under the terms of the BSD 3-Clause license.
# See the file 'LICENSE' in the root directory of the present distribution,
# or https://opensource.org/licenses/BSD-3-Clause
#
from .abstract_generator import AbstractGenerator


class PythonGenerator(AbstractGenerator):
    """
    Python code generic generator for XSD schemas.
    """
    formal_language = 'Python'

    default_paths = ['templates/python/']

    builtin_types = {
        'string': 'str',
        'boolean': 'bool',
        'float': 'float',
        'double': 'float',
        'integer': 'int',
        'unsignedByte': 'int',
        'nonNegativeInteger': 'int',
        'positiveInteger': 'int',
    }
#!/usr/bin/env python3
#
# Copyright (c) 2020, SISSA (Scuola Internazionale Superiore di Studi Avanzati).
# All rights reserved.
# This file is distributed under the terms of the BSD 3-Clause license.
# See the file 'LICENSE' in the root directory of the present distribution,
# or https://opensource.org/licenses/BSD-3-Clause
#
from .base import AbstractGenerator


class PythonGenerator(AbstractGenerator):
    """A Python code generator for XSD schemas."""
    templates_dir = 'templates/python/'

    builtin_types = {
        'string': 'str',
        'boolean': 'bool',
        'double': 'float',
        'integer': 'int',
        'unsignedByte': 'int',
        'nonNegativeInteger': 'int',
        'positiveInteger': 'int',
    }
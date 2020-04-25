#
# Copyright (c) 2020, Quantum Espresso Foundation and SISSA.
# Internazionale Superiore di Studi Avanzati). All rights reserved.
# This file is distributed under the terms of the BSD 3-Clause license.
# See the file 'LICENSE' in the root directory of the present distribution,
# or https://opensource.org/licenses/BSD-3-Clause
#
from .base import AbstractGenerator


class JSONSchemaGenerator(AbstractGenerator):
    """A JSON Schema generator for XSD schemas."""
    default_paths = ['templates/json-schema/']

    builtin_types = {
        'string': 'string',
        'boolean': 'boolean',
        'double': 'number',
        'integer': 'integer',
        'unsignedByte': 'integer',
        'nonNegativeInteger': 'integer',
        'positiveInteger': 'integer',
    }
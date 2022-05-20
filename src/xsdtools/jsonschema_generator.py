#
# Copyright (c) 2020, Quantum Espresso Foundation and SISSA.
# Internazionale Superiore di Studi Avanzati). All rights reserved.
# This file is distributed under the terms of the BSD 3-Clause license.
# See the file 'LICENSE' in the root directory of the present distribution,
# or https://opensource.org/licenses/BSD-3-Clause
#
from xmlschema.extras.codegen import AbstractGenerator


class JSONSchemaGenerator(AbstractGenerator):
    """
    JSON Schema generic generator for XSD schemas.
    """
    formal_language = 'JSON Schema'

    searchpaths = ['templates/json-schema/']

    builtin_types = {
        'string': 'string',
        'boolean': 'boolean',
        'float': 'number',
        'double': 'number',
        'integer': 'integer',
        'unsignedByte': 'integer',
        'nonNegativeInteger': 'integer',
        'positiveInteger': 'integer',
    }

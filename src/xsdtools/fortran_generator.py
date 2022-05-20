#
# Copyright (c) 2020, Quantum Espresso Foundation and SISSA.
# Internazionale Superiore di Studi Avanzati). All rights reserved.
# This file is distributed under the terms of the BSD 3-Clause license.
# See the file 'LICENSE' in the root directory of the present distribution,
# or https://opensource.org/licenses/BSD-3-Clause
#
from xmlschema.extras.codegen import AbstractGenerator


class FortranGenerator(AbstractGenerator):
    """
    Fortran code generic generator for XSD schemas.
    """
    formal_language = 'Fortran'

    searchpaths = ['templates/fortran/']

    builtin_types = {
        'string': 'CHARACTER(len=256)',
        'boolean': 'LOGICAL',
        'float': 'REAL(DP)',
        'double': 'REAL(DP)',
        'integer': 'INTEGER',
        'unsignedByte': 'INTEGER',
        'nonNegativeInteger': 'INTEGER',
        'positiveInteger': 'INTEGER',
    }

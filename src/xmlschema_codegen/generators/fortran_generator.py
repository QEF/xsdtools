#!/usr/bin/env python3
#
# Copyright (c) 2020, SISSA (Scuola Internazionale Superiore di Studi Avanzati).
# All rights reserved.
# This file is distributed under the terms of the BSD 3-Clause license.
# See the file 'LICENSE' in the root directory of the present distribution,
# or https://opensource.org/licenses/BSD-3-Clause
#
from xmlschema.qnames import local_name
from xmlschema.namespaces import XSD_NAMESPACE

from .base import filter_function, AbstractGenerator


XSD_BUILTINS_MAP = {
    'string': 'CHARACTER(len=256)',
    'boolean': 'LOGICAL',
    'double': 'REAL(DP)',
    'integer': 'INTEGER',
    'unsignedByte': 'INTEGER',
    'nonNegativeInteger': 'INTEGER',
    'positiveInteger': 'INTEGER',
}


def get_fortran_type(xsd_type):
    if xsd_type.target_namespace == XSD_NAMESPACE:
        return XSD_BUILTINS_MAP[local_name(xsd_type.name)]
    elif xsd_type.is_simple():
        print(xsd_type)
        breakpoint()
    return xsd_type.name


class FortranGenerator(AbstractGenerator):
    """A FORTRAN code generator for XSD schemas."""
    default_path = 'templates/fortran/'

    builtins_map = {
        'string': 'CHARACTER(len=256)',
        'boolean': 'LOGICAL',
        'double': 'REAL(DP)',
        'integer': 'INTEGER',
        'unsignedByte': 'INTEGER',
        'nonNegativeInteger': 'INTEGER',
        'positiveInteger': 'INTEGER',
    }

    @filter_function
    def fortran_type(self, xsd_type):
        if xsd_type.target_namespace == XSD_NAMESPACE:
            return self.types_map[local_name(xsd_type.name)]
        elif xsd_type.is_simple():
            print(xsd_type)
            breakpoint()
        return xsd_type.name

    filters = {
        'fortran_type': fortran_type,
    }
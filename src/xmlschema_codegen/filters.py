#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2020, SISSA (Scuola Internazionale Superiore di Studi Avanzati).
# All rights reserved.
# This file is distributed under the terms of the BSD 3-Clause license.
# See the file 'LICENSE' in the root directory of the present distribution,
# or https://opensource.org/licenses/BSD-3-Clause
#
from xmlschema.qnames import local_name
from xmlschema.namespaces import XSD_NAMESPACE


XSD_BUILTINS_TO_FORTRAN = {
    "string": "CHARACTER(len=256)",
    "boolean": "LOGICAL",
    "double": "REAL(DP)",
    "integer": "INTEGER",
    "unsignedByte": "INTEGER",
    "nonNegativeInteger": "INTEGER",
    "positiveInteger": "INTEGER",
    # "d2vectorType": "REAL(DP), DIMENSION(2)",
    # "d3vectorType": "REAL(DP), DIMENSION(3)",
    # "vectorType": "REAL(DP), DIMENSION(:), ALLOCATABLE",
    # "doubleListType": "REAL(DP), DIMENSION(:), ALLOCATABLE",
    # "matrixType": "REAL(DP), DIMENSION(:), ALLOCATABLE",
    # "smearingChoiceType": "CHARACTER(len=256)",
    # "integerListType": "INTEGER, DIMENSION(:), ALLOCATABLE",
    # "integerVectorType": "INTEGER, DIMENSION(:), ALLOCATABLE",
    # "constr_parms_listType": "REAL(DP), DIMENSION(4)",
    # "d3complexDType": "REAL(DP), DIMENSION(6)",
    # "disp_x_y_zType": "REAL(DP), DIMENSION(2)",
    # "cell_dimensionsType": "REAL(DP), DIMENSION(6)"
}


def get_fortran_type(xsd_type):
    if xsd_type.target_namespace == XSD_NAMESPACE:
        return XSD_BUILTINS_TO_FORTRAN[local_name(xsd_type.name)]
    elif xsd_type.is_simple():
        print(xsd_type)
        import pdb
        pdb.set_trace()
    return xsd_type.name

#
# Copyright (c) 2020, Quantum Espresso Foundation and SISSA.
# Internazionale Superiore di Studi Avanzati). All rights reserved.
# This file is distributed under the terms of the BSD 3-Clause license.
# See the file 'LICENSE' in the root directory of the present distribution,
# or https://opensource.org/licenses/BSD-3-Clause
#
from xmlschema.validators import XsdType, XsdElement, XsdAttribute
from ..helpers import filter_method
from ..fortran_generator import FortranGenerator


class QEFortranGenerator(FortranGenerator):
    """
    A Fortran code generator for Quantum ESPRESSO.
    """
    default_paths = ['templates/qe/']

    schema_types = {
        "d2vectorType": "REAL(DP), DIMENSION(2)",
        "d3vectorType": "REAL(DP), DIMENSION(3)",
        "vectorType": "REAL(DP), DIMENSION(:), ALLOCATABLE",
        "doubleListType": "REAL(DP), DIMENSION(:), ALLOCATABLE",
        "matrixType": "REAL(DP), DIMENSION(:), ALLOCATABLE",
        "smearingChoiceType": "CHARACTER(len=256)",
        "integerListType": "INTEGER, DIMENSION(:), ALLOCATABLE",
        "integerVectorType": "INTEGER, DIMENSION(:), ALLOCATABLE",
        "constr_parms_listType": "REAL(DP), DIMENSION(4)",
        "d3complexDType": "REAL(DP), DIMENSION(6)",
        "disp_x_y_zType": "REAL(DP), DIMENSION(2)",
        "cell_dimensionsType": "REAL(DP), DIMENSION(6)",
    }

    def __init__(self, schema, searchpath=None, filters=None, types_map=None):
        if types_map is None:
            types_map = self.schema_types
        else:
            types_map = self.schema_types.copy().update(**types_map)
        
        super(QEFortranGenerator, self).__init__(schema, searchpath, filters, types_map)

    @staticmethod
    @filter_method
    def type_name(obj):
        if isinstance(obj, XsdType):
            name = obj.local_name or ''
        elif isinstance(obj, (XsdAttribute, XsdElement)):
            name = obj.type.local_name or ''
        else:
            return ''

        return name[:-4] + '_type' if name.endswith('Type') else name

    @staticmethod
    @filter_method
    def read_function_name(xsd_type):
        if xsd_type.is_simple():
            return 'extractDataContent'
        return 'qes_read_' + xsd_type.local_name.replace('Type', '')

    @staticmethod
    @filter_method
    def bcast_function_name(xsd_type):
        return 'qes_bcast_' + xsd_type.local_name.replace('Type', '')

    @staticmethod
    @filter_method
    def init_function_name(xsd_type):
        name = xsd_type.local_name
        if name in ['matrixType', 'integerMatrixType']:
            return ', '.join(
                'qes_init_' + name.replace('Type', '_%d' % k) for k in (1, 2, 3)
            )
        elif xsd_type.is_complex():
            return 'qes_init_' + name.replace('Type', '')
        else:
            return None

    @staticmethod
    @filter_method
    def write_function_name(xsd_type):
        if xsd_type.is_simple():
            return "xml_addCharacters"
        return 'qes_write_' + xsd_type.local_name.replace('Type', '')

    @staticmethod
    @filter_method
    def reset_function_name(xsd_type):
        try:
            if xsd_type.is_complex():
                return 'qes_reset_' + xsd_type.local_name.replace('Type', '')
        except AttributeError:
            return
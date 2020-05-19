#
# Copyright (c) 2020, Quantum Espresso Foundation and SISSA.
# Internazionale Superiore di Studi Avanzati). All rights reserved.
# This file is distributed under the terms of the BSD 3-Clause license.
# See the file 'LICENSE' in the root directory of the present distribution,
# or https://opensource.org/licenses/BSD-3-Clause
#
import re

from xmlschema.validators import XsdType, XsdElement, XsdAttribute
from ..helpers import filter_method
from ..fortran_generator import FortranGenerator

QE_NAMESPACE = "http://www.quantum-espresso.org/ns/qes/qes-1.0"


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
        assert self.schema.target_namespace == QE_NAMESPACE

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
    def function_name(xsd_type):
        name = xsd_type.local_name or ''
        if name.endswith('Type'):
            return name.replace('Type', '')
        else:
            return name

    @filter_method
    def is_qes_array_type(self, xsd_type):
        if xsd_type.local_name in ("vectorType", "integerVectorType", "integerMatrixType"):
            return True
        elif xsd_type.is_derived(self.schema.types['vectorType']):
            return True
        elif xsd_type.is_derived(self.schema.types['integerVectorType']):
            return True
        elif xsd_type.is_derived(self.schema.types['integerMatrixType']):
            return True
        else:
            return False

    @staticmethod
    @filter_method
    def is_qes_type(xsd_type):
        return xsd_type.target_namespace == QE_NAMESPACE

    @staticmethod
    @filter_method
    def has_multi_sequence(xsd_type):
        if xsd_type.has_simple_content():
            return False
        return any(e.is_multiple() for e in xsd_type.content_type.iter_elements())

    @staticmethod
    @filter_method
    def reset_function_name(xsd_type):
        try:
            if xsd_type.is_complex():
                return 'qes_reset_' + xsd_type.local_name.replace('Type', '')
        except AttributeError:
            return

    @filter_method
    def init_fortran_type_name(self, xsd_type):
        tmp = re.sub(r'LEN=[\d]+', 'LEN=*', self.type_name(xsd_type), flags=re.IGNORECASE)
        return tmp.replace(', ALLOCATABLE','')

    @filter_method
    def init_extension_fortran_type(self, xsd_type):
        tmp = re.sub(r'LEN=[\d]+', 'LEN=*', self.type_name(xsd_type.base_type),
              flags=re.IGNORECASE)
        return tmp.replace(', ALLOCATABLE','')

    @staticmethod
    @filter_method
    def dimension(xsd_element):
        if xsd_element.max_occurs in (0, 1):
            return ''
        elif xsd_element.min_occurs == xsd_element.max_occurs:
            return 'DIMENSION({}),'.format(xsd_element.max_occurs)
        else:
            return 'DIMENSION(:),'

    @staticmethod
    @filter_method
    def init_argument_line(xsd_type):
        line_head = []
        line_tail = []
        indent = len('  SUBROUTINE qes_init_' + xsd_type.local_name.replace('Type', ''))
        if xsd_type.is_complex():
            for attribute in xsd_type.attributes.values():
                if attribute.is_required:
                    line_head.append(attribute.local_name)
                else:
                    line_tail.append(attribute.local_name)

        if not xsd_type.has_simple_content():
            for element in xsd_type.content_type.iter_elements():
                if element.min_occurs != 0:
                    line_head.append(element.tag)
                else:
                    line_tail.append(element.tag)

        if xsd_type.is_extension():
            line_head.append(xsd_type.local_name.replace('Type', ''))

        line = 'obj, tagname'
        lines=[]
        max_line = 90
        arglist = line_head + line_tail
        lastindex = len(line_head + line_tail) - 1
        for arg in line_head + line_tail:
            if len(line) + indent > max_line and arglist.index(arg) < lastindex:
                line = line + ',&'
                lines.append(line)
                line = ''
            if line == '':
                line = indent * ' ' + arg
                max_line = 90 + indent
            else:
                line += ', ' + arg
        max_line = 100
        if  len(line) > max_line:
            line += ' &'
            lines.append(line)
            lines.append(indent * ' ')
        else:
            lines.append(line)
        return '\n'.join(lines)

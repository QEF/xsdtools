#
# Copyright (c) 2020, Quantum Espresso Foundation and SISSA.
# Internazionale Superiore di Studi Avanzati). All rights reserved.
# This file is distributed under the terms of the BSD 3-Clause license.
# See the file 'LICENSE' in the root directory of the present distribution,
# or https://opensource.org/licenses/BSD-3-Clause
#
from ..base import filter_method
from ..fortran_generator import FortranGenerator


class QEFortranGenerator(FortranGenerator):
    """A FORTRAN code generator for Quantum ESPRESSO."""
    default_paths = ['templates/qe/']

    def render_files(self, output_dir, extensions=None, filter_func=None):
        if filter_func is None:
            super(QEFortranGenerator, self).render_files(
                output_dir, extensions, filter_func=lambda x: 'module' in x
            )
        else:
            super(QEFortranGenerator, self).render_files(output_dir, extensions, filter_func)

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


@QEFortranGenerator.register_filter
def reset_function_name(xsd_type):
    if xsd_type.is_complex():
        return 'qes_reset_' + xsd_type.local_name.replace('Type', '')

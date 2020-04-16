#!/usr/bin/env python3
#
# Copyright (c) 2020, SISSA (Scuola Internazionale Superiore di Studi Avanzati).
# All rights reserved.
# This file is distributed under the terms of the BSD 3-Clause license.
# See the file 'LICENSE' in the root directory of the present distribution,
# or https://opensource.org/licenses/BSD-3-Clause
#
"""
Temporary test script for Quantum ESPRESSO suite. Will be moved to QE's xmltool when completed.
"""

import unittest
import os
import xmlschema

from xmlschema_codegen import FortranGenerator


def resource_path(rel_path):
    resource_dir = os.path.join(os.path.dirname(__file__), 'resources')
    return os.path.join(resource_dir, rel_path)


##
# Filter functions for QES templates
#
def read_function_name(xsd_type):
    if xsd_type.is_simple():
        return 'extractDataContent'
    return 'qes_read_' + xsd_type.local_name.replace('Type', '')


def bcast_function_name(xsd_type):
    return 'qes_bcast_' + xsd_type.local_name.replace('Type', '')


def init_function_name(xsd_type):
    name = xsd_type.local_name
    if name in ['matrixType', 'integerMatrixType']:
       return ', '.join(
           'qes_init_' + name.replace('Type','_%d' % k) for k in (1, 2, 3)
       )
    elif xsd_type.is_complex():
       return 'qes_init_' + name.replace('Type','')
    else:
       return None


def write_function_name(xsd_type):
    if xsd_type.is_simple():
        return "xml_addCharacters"
    return 'qes_write_' + xsd_type.local_name.replace('Type', '')


def reset_function_name(xsd_type):
    if xsd_type.is_complex():
       return 'qes_reset_' + xsd_type.local_name.replace('Type','')


@unittest.skip
class TestEspressoPw(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        xsd_file = resource_path('schemas/qes.xsd')
        cls.schema = xmlschema.XMLSchema(xsd_file)
        cls.templates_dir = resource_path('templates/')
        cls.generator = FortranGenerator(cls.schema, searchpath=cls.templates_dir)

    def test_schema_object(self):
        components = [c for c in self.schema.iter_components()]
        self.assertEqual(len(components), 841)
        self.assertEqual(len(self.schema.elements), 1)
        self.assertIn('espresso', self.schema.elements)

    def test_generator_object(self):
        searchpath = os.path.abspath(self.templates_dir)
        self.assertEqual(
            repr(self.generator),
            "FortranGenerator(xsd_file='qes.xsd', searchpath='%s')" % searchpath
        )

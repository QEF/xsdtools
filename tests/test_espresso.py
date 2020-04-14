#!/usr/bin/env python3
#
# Copyright (c) 2020, SISSA (Scuola Internazionale Superiore di Studi Avanzati).
# All rights reserved.
# This file is distributed under the terms of the BSD 3-Clause license.
# See the file 'LICENSE' in the root directory of the present distribution,
# or https://opensource.org/licenses/BSD-3-Clause
#
import unittest
import os
import xmlschema

from xmlschema_codegen import FortranGenerator


def resource_path(rel_path):
    resource_dir = os.path.join(os.path.dirname(__file__), 'resources')
    return os.path.join(resource_dir, rel_path)


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
        searchpath = os.path.relpath(self.templates_dir)
        self.assertEqual(
            repr(self.generator),
            "FortranGenerator(xsd_file='qes.xsd', searchpath='%s')" % searchpath
        )

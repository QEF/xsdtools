#!/usr/bin/env python3
#
# Copyright (c) 2020, SISSA (Scuola Internazionale Superiore di Studi Avanzati).
# All rights reserved.
# This file is distributed under the terms of the BSD 3-Clause license.
# See the file 'LICENSE' in the root directory of the present distribution,
# or https://opensource.org/licenses/BSD-3-Clause
#
import unittest
import jinja2
import xmlschema

from xmlschema_generator import *


XSD_TEST = """
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
    <xs:element name="root" />
</xs:schema>
"""


class TestGenerators(unittest.TestCase):

    generators_classes = [
        FortranGenerator, CGenerator, PythonGenerator, JSONSchemaGenerator,
    ]

    @classmethod
    def setUpClass(cls):
        cls.schema = xmlschema.XMLSchema(XSD_TEST)

    def test_initialization(self):
        for cls in self.generators_classes:
            generator = cls(self.schema)
            self.assertIsInstance(generator, cls)
            self.assertIs(generator._schema, self.schema)
            self.assertIsInstance(generator._env, jinja2.Environment)

#
# Copyright (c) 2020, Quantum Espresso Foundation and SISSA.
# Internazionale Superiore di Studi Avanzati). All rights reserved.
# This file is distributed under the terms of the BSD 3-Clause license.
# See the file 'LICENSE' in the root directory of the present distribution,
# or https://opensource.org/licenses/BSD-3-Clause
#
import unittest
from pathlib import Path
import jinja2
import xmlschema

from xmlschema_codegen import *


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
            self.assertIs(generator.schema, self.schema)
            self.assertIsInstance(generator._env, jinja2.Environment)

    def test_get_template(self):
        codegen = FortranGenerator(self.schema)
        template = codegen.get_template('base.f90.jinja')
        with open(template.filename) as fp:
            self.assertNotIn("{# Override base90.f90 template #}", fp.read())

        searchpath = Path(__file__).absolute().parent.joinpath('templates/fortran/')
        self.assertTrue(searchpath.is_dir())

        codegen = FortranGenerator(self.schema, str(searchpath))
        template = codegen.get_template('base.f90.jinja')
        with open(template.filename) as fp:
            self.assertIn("{# Override base90.f90 template #}", fp.read())

    def test_list_templates(self):
        codegen = FortranGenerator(self.schema)
        self.assertListEqual(codegen.list_templates(),
                             ['base.f90.jinja', 'types_module.f90.jinja'])

        searchpath = Path(__file__).absolute().parent.joinpath('templates/fortran/')
        self.assertTrue(searchpath.is_dir())
        codegen = FortranGenerator(self.schema, str(searchpath))
        self.assertListEqual(
            codegen.list_templates(),
            ['base.f90.jinja', 'qes_types_module.f90.jinja', 'types_module.f90.jinja']
        )

    def test_render_files(self):
        codegen = FortranGenerator(self.schema)
        codegen.render_files('output/')

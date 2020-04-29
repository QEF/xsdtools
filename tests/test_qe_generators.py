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

from xmlschema_codegen import QEFortranGenerator


class TestQEGenerators(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.xsd_file = Path(__file__).absolute().parent.joinpath('schemas/qe/qes.xsd')
        cls.schema = xmlschema.XMLSchema(str(cls.xsd_file))

    def test_codegen_class(self):
        default_filters = ['to_type', 'read_function_name', 'bcast_function_name',
                           'init_function_name', 'write_function_name', 'reset_function_name']

        self.assertListEqual(list(QEFortranGenerator.default_filters), default_filters)

    def test_initialization(self):
        codegen = QEFortranGenerator(str(self.xsd_file))
        self.assertIsInstance(codegen.schema, xmlschema.XMLSchema)
        self.assertIsInstance(codegen._env, jinja2.Environment)

    def test_get_template(self):
        codegen = QEFortranGenerator(self.schema)
        template = codegen.get_template('base.f90.jinja')
        with open(template.filename) as fp:
            self.assertNotIn("{# Override base90.f90 template #}", fp.read())

        template = codegen.get_template('read/qes_read_module.f90.jinja')
        with open(template.filename) as fp:
            self.assertIn("MODULE qes_read_module", fp.read())

        searchpath = Path(__file__).absolute().parent.joinpath('templates/fortran/')
        self.assertTrue(searchpath.is_dir())

        codegen = QEFortranGenerator(self.schema, str(searchpath))
        template = codegen.get_template('base.f90.jinja')
        with open(template.filename) as fp:
            self.assertIn("{# Override base90.f90 template #}", fp.read())

    def test_list_templates(self):
        codegen = QEFortranGenerator(self.schema)
        templates = codegen.list_templates()

        self.assertIn('base.f90.jinja', templates)
        self.assertNotIn('qes_read_module.f90.jinja', templates)
        self.assertIn('read/qes_read_module.f90.jinja', templates)
        self.assertIn('types/qes_types_module.f90.jinja', templates)

        searchpath = Path(__file__).absolute().parent.joinpath('templates/fortran/')
        self.assertTrue(searchpath.is_dir())
        codegen = QEFortranGenerator(self.schema, str(searchpath))

        templates = codegen.list_templates()
        self.assertIn('base.f90.jinja', templates)
        self.assertIn('qes_types_module.f90.jinja', templates)
        self.assertIn('types/qes_types_module.f90.jinja', templates)

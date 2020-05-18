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


class TestQEFortranGenerator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.xsd_file = Path(__file__).absolute().parent.joinpath('schemas/qe/qes-refactored.xsd')
        cls.schema = xmlschema.XMLSchema(str(cls.xsd_file))

    def test_codegen_class(self):
        default_filters = [
            'local_name', 'qname', 'tag_name', 'type_name', 'namespace', 'sorted_types',
            'sorted_complex_types', 'read_function_name', 'bcast_function_name',
            'init_function_name', 'write_function_name', 'reset_function_name'
        ]
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

    def test_render_types_module(self):
        qe_generator = QEFortranGenerator(self.schema)
        result = qe_generator.render('types/qes_types_module.f90.jinja')[0]
        self.assertIsInstance(result, str)
        result_lines = result.split('\n')

        type_module = Path(__file__).absolute().parent.joinpath('samples/qe/qes_types_module.f90')
        with type_module.open() as fp:
            type_module_lines = fp.read().split('\n')

        for k in range(min(len(result_lines), len(type_module_lines))):
            line1 = result_lines[k]
            line2 = type_module_lines[k]
            self.assertEqual(
                line1, line2, msg="Line {}-{}: {!r}".format(
                    k + 1, k + 6, '\n'.join(result_lines[k:k + 5])
                ))

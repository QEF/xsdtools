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
import datetime

from xmlschema_codegen import *
from xmlschema_codegen.helpers import xsd_qname


XSD_TEST = """
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:tns="http://codegen.test/0" targetNamespace="http://codegen.test/0">
  <xs:element name="root" type="xs:string" />
</xs:schema>
"""


class DemoGenerator(AbstractGenerator):
    formal_language = 'Demo'

    default_paths = ['templates/filters/']

    builtin_types = {
        'anyType': '',
        'anySimpleType': '',
        'string': 'str',
        'boolean': 'bool',
        'float': 'float',
        'double': 'double',
        'integer': 'int',
        'unsignedByte': 'unsigned short',
        'nonNegativeInteger': 'unsigned int',
        'positiveInteger': 'unsigned int',
    }

    @classmethod
    @filter_method
    def class_filter(cls, obj):
        return str(obj)

    @staticmethod
    @filter_method
    def static_filter(obj):
        return str(obj)

    @filter_method
    def instance_filter(self, obj):
        return str(obj)


@DemoGenerator.register_filter
def function_filter(obj):
    return str(obj)


class TestDemoGenerator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.schema = xmlschema.XMLSchema(XSD_TEST)

    def test_initialization(self):
        generator = DemoGenerator(self.schema)
        self.assertIs(generator.schema, self.schema)
        self.assertIsInstance(generator._env, jinja2.Environment)

    def test_formal_language(self):
        self.assertEqual(DemoGenerator.formal_language, 'Demo')

    def test_builtin_types(self):
        generator = DemoGenerator(self.schema)
        self.assertIn(xsd_qname('anyType'), generator.builtin_types)
        self.assertIn(xsd_qname('string'), generator.builtin_types)
        self.assertIn(xsd_qname('float'), generator.builtin_types)
        self.assertIsNot(generator.builtin_types, generator.types_map)
        self.assertEqual(generator.builtin_types, generator.types_map)

    def test_demo_filters(self):
        codegen = DemoGenerator(self.schema)

        dt = datetime.datetime(1999, 12, 31, 23, 59, 59)
        self.assertEqual(codegen.filters['instance_filter'](dt), '1999-12-31 23:59:59')
        self.assertEqual(codegen.filters['static_filter'](dt), '1999-12-31 23:59:59')
        self.assertEqual(codegen.filters['class_filter'](dt), '1999-12-31 23:59:59')
        self.assertEqual(codegen.filters['function_filter'](dt), '1999-12-31 23:59:59')

        searchpath = Path(__file__).absolute().parent.joinpath('templates/filters/')
        codegen = DemoGenerator(self.schema, str(searchpath))
        self.assertListEqual(codegen.render('local_name_filter_test.jinja'), ['root'])
        self.assertListEqual(codegen.render('demo_type_filter_test.jinja'), ['str'])


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
        codegen.render_to_files(names=[], output_dir='output/')

    def test_formal_language(self):
        self.assertEqual(CGenerator.formal_language, 'C')
        self.assertEqual(FortranGenerator.formal_language, 'Fortran')
        self.assertEqual(PythonGenerator.formal_language, 'Python')
        self.assertEqual(JSONSchemaGenerator.formal_language, 'JSON Schema')

    def test_filters2(self):
        searchpath = Path(__file__).absolute().parent.joinpath('templates/filters/')
        codegen = FortranGenerator(self.schema, str(searchpath))

        self.assertListEqual(codegen.render('local_name_filter_test.jinja'), ['root'])
        self.assertListEqual(
            codegen.render('fortran_type_filter_test.jinja'), ['CHARACTER(len=256)']
        )

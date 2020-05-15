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


class TestAbstractGenerator(unittest.TestCase):

    generator_class = DemoGenerator

    @classmethod
    def setUpClass(cls):
        cls.schema = xmlschema.XMLSchema(XSD_TEST)
        cls.searchpath = Path(__file__).absolute().parent.joinpath('templates/filters/')
        cls.generator = cls.generator_class(cls.schema, str(cls.searchpath))

    def test_initialization(self):
        generator = self.generator_class(self.schema)
        self.assertIs(generator.schema, self.schema)
        self.assertIsInstance(generator._env, jinja2.Environment)

    def test_formal_language(self):
        self.assertEqual(self.generator_class.formal_language, 'Demo')

    def test_builtin_types(self):
        generator = self.generator_class(self.schema)
        self.assertIn(xsd_qname('anyType'), generator.builtin_types)
        self.assertIn(xsd_qname('string'), generator.builtin_types)
        self.assertIn(xsd_qname('float'), generator.builtin_types)
        self.assertIsNot(generator.builtin_types, generator.types_map)
        self.assertEqual(generator.builtin_types, generator.types_map)

    def test_language_default_filters(self):
        demo_gen = DemoGenerator(self.schema)

        dt = datetime.datetime(1999, 12, 31, 23, 59, 59)
        self.assertEqual(demo_gen.filters['instance_filter'](dt), '1999-12-31 23:59:59')
        self.assertEqual(demo_gen.filters['static_filter'](dt), '1999-12-31 23:59:59')
        self.assertEqual(demo_gen.filters['class_filter'](dt), '1999-12-31 23:59:59')
        self.assertEqual(demo_gen.filters['function_filter'](dt), '1999-12-31 23:59:59')

        self.assertListEqual(self.generator.render('demo_type_filter_test.jinja'), ['str'])

    def test_generic_default_filters(self):
        self.assertListEqual(self.generator.render('local_name_filter_test.jinja'), ['root'])


class TestCGenerator(TestAbstractGenerator):

    generator_class = CGenerator

    def test_formal_language(self):
        self.assertEqual(self.generator_class.formal_language, 'C')

    def test_language_default_filters(self):
        self.assertListEqual(self.generator.render('c_type_filter_test.jinja'), ['str'])


class TestFortranGenerator(TestAbstractGenerator):

    generator_class = FortranGenerator

    def test_formal_language(self):
        self.assertEqual(self.generator_class.formal_language, 'Fortran')

    def test_language_default_filters(self):
        self.assertListEqual(
            self.generator.render('fortran_type_filter_test.jinja'), ['CHARACTER(len=256)']
        )

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

    @unittest.skip('FIXME')
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


class TestPythonGenerator(TestAbstractGenerator):

    generator_class = PythonGenerator

    def test_formal_language(self):
        self.assertEqual(self.generator_class.formal_language, 'Python')

    def test_language_default_filters(self):
        self.assertListEqual(
            self.generator.render('python_type_filter_test.jinja'), ['str']
        )


class TestJSONSchemaGenerator(TestAbstractGenerator):

    generator_class = JSONSchemaGenerator

    def test_formal_language(self):
        self.assertEqual(self.generator_class.formal_language, 'JSON Schema')

    def test_language_default_filters(self):
        self.assertListEqual(
            self.generator.render('json_schema_type_filter_test.jinja'), ['string']
        )

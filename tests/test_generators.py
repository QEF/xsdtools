#
# Copyright (c) 2020, Quantum Espresso Foundation and SISSA.
# Internazionale Superiore di Studi Avanzati). All rights reserved.
# This file is distributed under the terms of the BSD 3-Clause license.
# See the file 'LICENSE' in the root directory of the present distribution,
# or https://opensource.org/licenses/BSD-3-Clause
#
import unittest
from pathlib import Path
import datetime

import jinja2
from xmlschema import XMLSchema
from xmlschema.extras.codegen import AbstractGenerator, xsd_qname, filter_method, PythonGenerator

# noinspection PyUnresolvedReferences
from xsdtools import CGenerator, FortranGenerator, JSONSchemaGenerator


XSD_TEST = """
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:tns="http://codegen.test/0" targetNamespace="http://codegen.test/0">
  <xs:element name="root" type="xs:string" />
  <xs:complexType name="type3">
    <xs:sequence>
      <xs:element name="elem1" type="tns:type1" />
      <xs:element name="elem2" type="tns:type2" />
    </xs:sequence>
  </xs:complexType>
  <xs:complexType name="type2">
    <xs:sequence>
      <xs:element name="elem1" type="tns:type1" />
      <xs:element name="elem4" type="tns:type4" />
    </xs:sequence>
  </xs:complexType>
  <xs:simpleType name="type4">
    <xs:restriction base="xs:string" />
  </xs:simpleType>
  <xs:complexType name="type1" />
</xs:schema>
"""


class DemoGenerator(AbstractGenerator):
    formal_language = 'Demo'

    searchpaths = ['templates/filters/']

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


class TestAbstractGenerator(unittest.TestCase):

    generator_class = DemoGenerator

    schema: XMLSchema
    searchpath: Path

    @classmethod
    def setUpClass(cls):
        cls.schema = XMLSchema(XSD_TEST)
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

    def test_language_type_filter(self):
        self.assertListEqual(self.generator.render('demo_type_filter_test.jinja'), ['str'])

    def test_filter_decorators(self):
        dt = datetime.datetime(1999, 12, 31, 23, 59, 59)

        if self.generator_class is DemoGenerator:
            demo_gen = DemoGenerator(self.schema)
            self.assertEqual(demo_gen.filters['instance_filter'](dt), '1999-12-31 23:59:59')
            self.assertEqual(demo_gen.filters['static_filter'](dt), '1999-12-31 23:59:59')
            self.assertEqual(demo_gen.filters['class_filter'](dt), '1999-12-31 23:59:59')
        else:
            with self.assertRaises(KeyError):
                self.generator.filters['instance_filter'](dt)

    def test_name_filter(self):
        xsd_element = self.schema.elements['root']
        self.assertEqual(self.generator.filters['name'](xsd_element), 'root')
        self.assertListEqual(self.generator.render('name_filter_test.jinja'), ['root'])

    def test_qname_filter(self):
        xsd_element = self.schema.elements['root']
        self.assertEqual(self.generator.filters['qname'](xsd_element), 'tns__root')
        self.assertListEqual(self.generator.render('qname_filter_test.jinja'), ['tns__root'])

    def test_namespace_filter(self):
        xsd_element = self.schema.elements['root']
        tns = 'http://codegen.test/0'
        self.assertEqual(self.generator.filters['namespace'](xsd_element), tns)
        self.assertListEqual(self.generator.render('namespace_filter_test.jinja'), [tns])

    def test_type_name_filter(self):
        xsd_element = self.schema.elements['root']
        self.assertEqual(self.generator.filters['type_name'](xsd_element), 'string')
        self.assertListEqual(self.generator.render('type_name_filter_test.jinja'), ['string'])

    def test_type_qname_filter(self):
        xsd_element = self.schema.elements['root']
        self.assertEqual(self.generator.filters['type_qname'](xsd_element), 'xs__string')
        self.assertListEqual(
            self.generator.render('type_qname_filter_test.jinja'), ['xs__string'])

    def test_sort_types_filter(self):
        xsd_types = self.schema.types
        self.assertListEqual(
            self.generator.filters['sort_types'](xsd_types),
            [xsd_types['type4'], xsd_types['type1'], xsd_types['type2'], xsd_types['type3']]
        )
        self.assertListEqual(
            self.generator.render('sort_types_filter_test.jinja'), ['type4type1type2type3']
        )

    def test_extension_test(self):
        pass


class TestCGenerator(TestAbstractGenerator):

    generator_class = CGenerator

    def test_formal_language(self):
        self.assertEqual(self.generator_class.formal_language, 'C')

    def test_language_type_filter(self):
        self.assertListEqual(self.generator.render('c_type_filter_test.jinja'), ['str'])


class TestFortranGenerator(TestAbstractGenerator):

    generator_class = FortranGenerator

    def test_formal_language(self):
        self.assertEqual(self.generator_class.formal_language, 'Fortran')

    def test_language_type_filter(self):
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

    def test_language_type_filter(self):
        self.assertListEqual(
            self.generator.render('python_type_filter_test.jinja'), ['str']
        )


class TestJSONSchemaGenerator(TestAbstractGenerator):

    generator_class = JSONSchemaGenerator

    def test_formal_language(self):
        self.assertEqual(self.generator_class.formal_language, 'JSON Schema')

    def test_language_type_filter(self):
        self.assertListEqual(
            self.generator.render('json_schema_type_filter_test.jinja'), ['string']
        )

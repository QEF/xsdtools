#!/usr/bin/env python3
#
# Copyright (c) 2020, SISSA (Scuola Internazionale Superiore di Studi Avanzati).
# All rights reserved.
# This file is distributed under the terms of the BSD 3-Clause license.
# See the file 'LICENSE' in the root directory of the present distribution,
# or https://opensource.org/licenses/BSD-3-Clause
#
import os
from abc import ABC
from jinja2 import Environment, ChoiceLoader, FileSystemLoader
import xmlschema

environments = {

}

class AbstractGenerator(ABC):

    templates_dir = None

    def __init__(self, schema, searchpath=None):
        assert isinstance(schema, xmlschema.XMLSchemaBase)
        self._schema = schema

        if searchpath is None:
            loader = FileSystemLoader(self.templates_dir)
        else:
            assert isinstance(searchpath, str)
            loader = ChoiceLoader([
                FileSystemLoader(searchpath),
                FileSystemLoader(self.templates_dir),
            ])

        self._env = Environment(loader=loader)

    def __repr__(self):
        return '%s(xsd_file=%r, searchpath=%r)' % (
            self.__class__.__name__, self.xsd_file, self.searchpath
        )

    @property
    def xsd_file(self):
        url = self._schema.url
        return os.path.basename(url) if url else None

    @property
    def searchpath(self):
        loaders = self._env.loader.loaders
        if len(loaders) <= 1:
            return
        return os.path.relpath(loaders[0].searchpath[0])


class CGenerator(AbstractGenerator):
    """An C code generator for XSD schemas."""
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates/c/')


class FortranGenerator(AbstractGenerator):
    """An FORTRAN code generator for XSD schemas."""
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates/fortran/')


class PythonGenerator(AbstractGenerator):
    """An Python code generator for XSD schemas."""
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates/python/')


class JSONSchemaGenerator(AbstractGenerator):
    """A JSON Schema generator for XSD schemas."""
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates/json-schema/')



def generate(args):
    """Generate code for an XSD schema."""
    print(args)

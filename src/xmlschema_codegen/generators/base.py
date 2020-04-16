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
from pathlib import Path
from jinja2 import Environment, ChoiceLoader, FileSystemLoader

import xmlschema

XSD_NAMESPACE = "http://www.w3.org/2001/XMLSchema"


def xsd_qname(name):
    return '{http://www.w3.org/2001/XMLSchema}%s' % name


def filter_function(func):
    """Mark the function for using as an additional filter."""
    func.is_filter = True
    return func


class AbstractGenerator(ABC):
    """
    Abstract base class for code generators. A generator works using the
    Jinja2 template engine by an Environment instance.

    :param schema: the XSD schema instance.
    :param searchpath: directory path for custom templates.
    :param filters: a dictionary with custom filter functions.
    :param types_map: a dictionary with custom mapping for XSD types.
    """
    templates_dir = None
    """Generator default template directory."""

    filters = None
    """Generator default filter functions."""

    builtins_map = None
    """Translation map for XSD builtin types."""

    def __init__(self, schema, searchpath=None, filters=None, types_map=None):
        assert isinstance(schema, xmlschema.XMLSchemaBase)
        self._schema = schema

        default_path = Path(__file__).absolute().parent.parent.joinpath(self.templates_dir)
        if not default_path.is_dir():
            raise ValueError("Invalid path {!r} for templates!".format(str(default_path)))

        if searchpath is None:
            loader = FileSystemLoader(str(default_path))
        else:
            assert isinstance(searchpath, str)
            loader = ChoiceLoader([
                FileSystemLoader(searchpath),
                FileSystemLoader(str(default_path)),
            ])

        filters = dict(filters) if filters else {}
        if self.filters:
            filters.update((k, v) for k, v in self.filters.items() if k not in filters)

        if self.builtins_map:
            self.types_map = {xsd_qname(k): v for k, v in self.builtins_map.items()}
        else:
            self.types_map = {}
        if types_map:
            self.types_map.update(types_map)

        self._env = Environment(loader=loader)
        self._env.filters.update(filters)

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

    def get_template(self, name):
        return self._env.get_template(name)

    def list_templates(self):
        return self._env.list_templates()


def generate(args):
    """Generate code for an XSD schema."""
    print(args)

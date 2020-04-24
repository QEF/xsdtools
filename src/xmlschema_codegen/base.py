#!/usr/bin/env python3
#
# Copyright (c) 2020, SISSA (Scuola Internazionale Superiore di Studi Avanzati).
# All rights reserved.
# This file is distributed under the terms of the BSD 3-Clause license.
# See the file 'LICENSE' in the root directory of the present distribution,
# or https://opensource.org/licenses/BSD-3-Clause
#
import os
import inspect
from abc import ABC, ABCMeta
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


class GeneratorMeta(ABCMeta):
    """Metaclass for creating code generators."""

    def __new__(mcs, name, bases, attrs):
        filters = {}
        builtins_map = {}
        for base in bases:
            if hasattr(base, 'default_filters'):
                filters.update(base.default_filters)
            if getattr(base, 'builtins_map', None):
                builtins_map.update(base.builtins_map)

        try:
            path = Path(__file__).absolute().parent.joinpath(attrs['default_path'])
        except (KeyError, TypeError):
            pass
        else:
            if not path.is_dir():
                raise ValueError("Path {!r} is not a directory!".format(str(path)))
            attrs['default_path'] = path

        try:
            for k, v in attrs['builtins_map'].items():
                builtins_map[xsd_qname(k)] = v
        except (KeyError, AttributeError):
            pass
        finally:
            attrs['builtins_map'] = builtins_map

        for k, v in attrs.items():
            if inspect.isfunction(v) and getattr(v, 'is_filter', False):
                filters[k] = v
        attrs['default_filters'] = filters

        return type.__new__(mcs, name, bases, attrs)


class AbstractGenerator(ABC, metaclass=GeneratorMeta):
    """
    Abstract base class for code generators. A generator works using the
    Jinja2 template engine by an Environment instance.

    :param schema: the XSD schema instance.
    :param searchpath: additional search path for custom templates.
    :param filters: additional custom filter functions.
    :param types_map: a dictionary with custom mapping for XSD types.
    """

    default_path = None
    """Default path for templates."""

    default_filters = None
    """Default filter functions."""

    builtins_map = None
    """Translation map for XSD builtin types."""

    def __init__(self, schema, searchpath=None, filters=None, types_map=None):
        assert isinstance(schema, xmlschema.XMLSchemaBase)
        self.schema = schema

        self.searchpath = searchpath
        if searchpath is None:
            loader = FileSystemLoader(str(self.default_path))
        else:
            assert isinstance(searchpath, str)
            loader = ChoiceLoader([
                FileSystemLoader(searchpath),
                FileSystemLoader(str(self.default_path)),
            ])

        self.types_map = self.builtins_map.copy()
        if types_map:
            self.types_map.update(types_map)

        self._env = Environment(loader=loader)
        self._env.filters.update(self.default_filters)
        self.filters = filters
        if filters:
            self._env.filters.update(filters)

    def __repr__(self):
        return '%s(xsd_file=%r, searchpath=%r)' % (
            self.__class__.__name__, self.xsd_file, self.searchpath
        )

    @property
    def xsd_file(self):
        url = self.schema.url
        return os.path.basename(url) if url else None

    def get_template(self, name):
        return self._env.get_template(name)

    def list_templates(self):
        return self._env.list_templates()

    @filter_function
    def to_type(self, xsd_type):
        try:
            return self.types_map[xsd_type.name]
        except KeyError:
            return xsd_type.name or ''


def generate(args):
    """Generate code for an XSD schema."""
    print(args)

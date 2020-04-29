#
# Copyright (c) 2020, Quantum Espresso Foundation and SISSA.
# Internazionale Superiore di Studi Avanzati). All rights reserved.
# This file is distributed under the terms of the BSD 3-Clause license.
# See the file 'LICENSE' in the root directory of the present distribution,
# or https://opensource.org/licenses/BSD-3-Clause
#
import os
import sys
import inspect
from abc import ABC, ABCMeta
from pathlib import Path
from jinja2 import Environment, ChoiceLoader, FileSystemLoader

import xmlschema

XSD_NAMESPACE = "http://www.w3.org/2001/XMLSchema"


def xsd_qname(name):
    return '{http://www.w3.org/2001/XMLSchema}%s' % name


def filter_method(func):
    """Marks a method for registration as template filter."""
    func.is_filter = True
    return func


class GeneratorMeta(ABCMeta):
    """Metaclass for creating code generators."""

    def __new__(mcs, name, bases, attrs):
        module = attrs['__module__']
        module_path = sys.modules[module].__file__

        default_paths = []
        default_filters = {}
        builtins_map = {}
        for base in bases:
            if getattr(base, 'default_paths', None):
                default_paths.extend(base.default_paths)
            if hasattr(base, 'default_filters'):
                default_filters.update(base.default_filters)
            if getattr(base, 'builtins_map', None):
                builtins_map.update(base.builtins_map)

        try:
            for path in attrs['default_paths']:
                if Path(path).is_absolute():
                    dirpath = Path(path)
                else:
                    dirpath = Path(module_path).parent.joinpath(path)

                if not dirpath.is_dir():
                    raise ValueError("Path {!r} is not a directory!".format(str(path)))
                default_paths.append(dirpath)

        except (KeyError, TypeError):
            pass
        else:
            attrs['default_paths'] = default_paths

        for k, v in attrs.items():
            if inspect.isfunction(v):
                if getattr(v, 'is_filter', False):
                    default_filters[k] = v
            elif inspect.isroutine(v):
                # static and class methods
                if getattr(v.__func__, 'is_filter', False):
                    default_filters[k] = v

        attrs['default_filters'] = default_filters

        try:
            for k, v in attrs['builtins_map'].items():
                builtins_map[xsd_qname(k)] = v
        except (KeyError, AttributeError):
            pass
        finally:
            attrs['builtins_map'] = builtins_map

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

    default_paths = None
    """Default paths for templates."""

    default_filters = None
    """Default filter functions."""

    builtins_map = None
    """Translation map for XSD builtin types."""

    def __init__(self, schema, searchpath=None, filters=None, types_map=None):
        if isinstance(schema, xmlschema.XMLSchemaBase):
            self.schema = schema
        else:
            self.schema = xmlschema.XMLSchema(schema)

        self.searchpath = searchpath
        file_loaders = []
        if searchpath is not None:
            file_loaders.append(FileSystemLoader(searchpath))
        if isinstance(self.default_paths, list):
            file_loaders.extend(
                FileSystemLoader(str(path)) for path in reversed(self.default_paths)
            )

        if not file_loaders:
            raise ValueError("At least one search path required for generator instance!")
        loader = ChoiceLoader(file_loaders) if len(file_loaders) > 1 else file_loaders[0]

        self._env = Environment(loader=loader)
        self._env.filters.update(self.default_filters)
        self.filters = filters
        if filters:
            self._env.filters.update(filters)

        self.types_map = self.builtins_map.copy()
        if types_map:
            self.types_map.update(types_map)

    def __repr__(self):
        return '%s(xsd_file=%r, searchpath=%r)' % (
            self.__class__.__name__, self.xsd_file, self.searchpath
        )

    @classmethod
    def register_filter(cls, func):
        """Registers a function as default filter for the code generator."""
        cls.default_filters[func.__name__] = func
        func.is_filter = True
        return func

    @property
    def xsd_file(self):
        url = self.schema.url
        return os.path.basename(url) if url else None

    def get_template(self, name):
        return self._env.get_template(name)

    def list_templates(self, extensions=None, filter_func=None):
        return self._env.list_templates(extensions, filter_func)

    def render_files(self, output_dir, extensions=None, filter_func=None):
        output_dir = Path(output_dir)
        for template_name in self._env.list_templates(extensions, filter_func):
            print(template_name)
            template = self.get_template(template_name)
            result = template.render(xsd_schema=self.schema)
            continue
            with open(output_file, 'w') as text_file:
                text_file.write(result)

    @filter_method
    def to_type(self, xsd_type):
        try:
            return self.types_map[xsd_type.name]
        except KeyError:
            return xsd_type.name or ''


def generate(args):
    """Generate code for an XSD schema."""
    print(args)

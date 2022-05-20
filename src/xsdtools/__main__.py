#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2020, Quantum Espresso Foundation and SISSA.
# Internazionale Superiore di Studi Avanzati). All rights reserved.
# This file is distributed under the terms of the BSD 3-Clause license.
# See the file 'LICENSE' in the root directory of the present distribution,
# or https://opensource.org/licenses/BSD-3-Clause
#
import sys
import os
import argparse
import logging
import pathlib

from xmlschema import XMLSchema, XMLSchema11
from xmlschema.cli import xsd_version_number, get_loglevel
from xmlschema.exceptions import XMLSchemaValueError

from xmlschema.extras.codegen import PythonGenerator, is_shell_wildcard
from xsdtools import CGenerator, FortranGenerator, QEFortranGenerator


PROGRAM_NAME = os.path.basename(sys.argv[0])

GENERATORS_MAP = {
    'C': CGenerator,
    'Fortran': FortranGenerator,
    'Python': PythonGenerator,
    'QE': QEFortranGenerator,
}


def get_generator_class(name):
    try:
        return GENERATORS_MAP[name]
    except KeyError:
        raise ValueError("--generator name must be in {!r}".format_map(list(GENERATORS_MAP)))


def main():
    parser = argparse.ArgumentParser(prog=PROGRAM_NAME, add_help=True,
                                     description="generate code for an XSD schema.")
    parser.usage = "%(prog)s [OPTION]... [FILE]...\n" \
                   "Try '%(prog)s --help' for more information."

    parser.add_argument('-v', dest='verbosity', action='count', default=0,
                        help="increase output verbosity.")
    parser.add_argument('--schema', type=str, metavar='PATH', required=True,
                        help="path or URL to an XSD schema.")
    parser.add_argument('--version', type=xsd_version_number, default='1.0',
                        help="XSD schema validator to use (default is 1.0).")
    parser.add_argument('-L', dest='locations', nargs=2, type=str, action='append',
                        metavar="URI/URL", help="schema location hint overrides.")
    parser.add_argument('--generator', type=str, metavar='NAME', required=True,
                        help="the generator to use. Option value can be one of "
                             "{!r}.".format(tuple(GENERATORS_MAP)))
    parser.add_argument('-o', '--output', type=str, default='.', metavar='DIRECTORY',
                        help="where to write the rendered files, current dir by default.")
    parser.add_argument('-f', '--force', action="store_true", default=False,
                        help="do not prompt before overwriting.")
    parser.add_argument('files', metavar='[TEMPLATE_FILE ...]',
                        nargs='*', help="Jinja template files to be rendered.")

    args = parser.parse_args()

    loglevel = get_loglevel(args.verbosity)
    logger = logging.getLogger('xsdtools')
    logger.setLevel(loglevel)

    schema_class = XMLSchema if args.version == '1.0' else XMLSchema11
    if args.schema is not None:
        schema = schema_class(args.schema, locations=args.locations, loglevel=loglevel)
    else:
        schema = None

    generator_class = get_generator_class(args.generator)
    base_path = pathlib.Path(args.output)
    if not base_path.exists():
        base_path.mkdir()
    elif not base_path.is_dir():
        raise XMLSchemaValueError("{!r} is not a directory".format(str(base_path)))

    template_files = {None: []}
    for path in map(pathlib.Path, args.files):
        if is_shell_wildcard(str(path)):
            template_files[None].append(str(path))
        elif path.suffix not in ('.jinja', '.j2', '.jinja2'):
            pass
        elif path.is_file():
            try:
                template_files[str(path.parent)].append(path.name)
            except KeyError:
                template_files[str(path.parent)] = [path.name]
        else:
            template_files[None].append(str(path))

    rendered_templates = []
    for searchpath, names in template_files.items():
        generator = generator_class(schema, searchpath)
        rendered_templates.extend(generator.render_to_files(
            names, output_dir=args.output, force=args.force
        ))

    print("Rendered n.{} files ...".format(len(rendered_templates)))
    sys.exit(not rendered_templates)


if __name__ == '__main__':
    if sys.version_info < (3, 7, 0):
        sys.stderr.write("You need python 3.7 or later to run this program\n")
        sys.exit(1)

    main()

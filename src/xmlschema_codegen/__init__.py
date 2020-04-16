#!/usr/bin/env python3
#
# Copyright (c) 2020, SISSA (Scuola Internazionale Superiore di Studi Avanzati).
# All rights reserved.
# This file is distributed under the terms of the BSD 3-Clause license.
# See the file 'LICENSE' in the root directory of the present distribution,
# or https://opensource.org/licenses/BSD-3-Clause
#
from .generators import AbstractGenerator, CGenerator, \
    FortranGenerator, PythonGenerator, JSONSchemaGenerator


_environments = {

}

def generate(xsd_file, template_file, output_file):
    """
    namespaces={"s":"http://www.w3.org/2001/XMLSchema"}
    xsd_schema = XSDSchema( input_xsd_file, namespaces )

    template_dir = os.path.dirname(template_file)
    template_filename = os.path.basename(template_file)
    template = Environment(
        loader=FileSystemLoader(template_dir)
    ).get_template(template_filename)


    result = template.render(xsd_schema=xsd_schema)

    with open(output_file, "w") as text_file:
        text_file.write(result)
    """


__all__ = ['AbstractGenerator', 'CGenerator', 'FortranGenerator', 'PythonGenerator',
           'JSONSchemaGenerator', 'generate']
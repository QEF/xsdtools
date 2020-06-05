*****************
xmlschema-codegen
*****************

.. introduction-start

This is a code generator software from XSD schemas. The generator engine
uses XSD schemas and Jinja2 templates to produce code and structures.

The generator requires Python 3.7+ for working and is based on the libraries
`xmlschema <https://github.com/brunato/xmlschema>`_ for processing XSD schemas
and `Jinja2 <https://github.com/pallets/jinja>`_ for processing templates.

The package can be used as a library in your Python code or by a console command
in generic shell scripts. Thought as experimental code for generating Fortran
interfaces for the XML schema-based data of Quantum ESPRESSO simulation suite,
it's opened to contributions on developing other languages or other template set.


Installation
============

First clone the project and then switch into its directory::

  git clone https://github.com/QEF/xmltool_dev.git xmlschema-codegen/
  cd xmlschema-codegen/

If you can create a virtual environment for this project, activate it and then run the command::

  pip install .

otherwise install the package in user space, avoiding root installations::

  pip install --user .


.. note::
    For source installations the `setuptools <https://github.com/pypa/setuptools>`_
    package is required.


Usage
=====

From command line::

  xmlschema-codegen --help

From Python console or module::

  from xmlschema_codegen import FortranGenerator
  codegen = FortranGenerator('schema.xsd')
  codegen.render_to_files('*', output_dir='./output')

You can provide your own templates through *searchpath* argument::

  codegen = FortranGenerator('schema.xsd', searchpath='./templates')
  codegen.render_to_files('my_template.jinja', output_dir='./output')


License
=======

This software is distributed under the terms of the BSD 3-Clause License.
See the file 'LICENSE' in the root directory of the present distribution,
or https://opensource.org/licenses/BSD-3-Clause.

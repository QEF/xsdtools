#################
xmlschema-codegen
#################

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
------------

Within a virtual environment simply type::

  pip install xmlschema-codegen

otherwise install the package in user space, avoiding root installations::

  pip install --user xmlschema-codegen

For installing from source within a virtual environment execute::

  git clone https://github.com/sissaschool/xmlschema-codegen.git
  cd xmlschema-codegen/
  python setup.py install

.. note::
    For source installations the `setuptools <https://github.com/pypa/setuptools>`_
    package is required.


Usage
-----

From command line::

  xmlschema-codegen --help

From Python console or module::

  import xmlschema_codegen as xcg

or::

  from xmlschema_codegen import generate


License
-------

This software is distributed under the terms of the BSD 3-Clause License.
See the file 'LICENSE' in the root directory of the present distribution,
or https://opensource.org/licenses/BSD-3-Clause.

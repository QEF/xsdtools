###################
xmlschema-generator
###################

This package is a code generator from XSD schemas. The generator engine
uses XSD schemas and Jinja2 templates to produce code and structures.

The generator requires Python 3.5+ for working and is based on the libraries
`xmlschema <https://github.com/brunato/xmlschema>`_ for processing XSD schemas
and `Jinja2 <https://github.com/pallets/jinja>`_ for processing templates.


Installation
------------

Within a virtual environment simply type::

  pip install xmlschema-generator

otherwise avoid root installations, so use::

  pip install --user xmlschema-generator

For installing from source within a virtual environment execute::

  python setup install

or otherwise for user space installations::

  python setup install --user

.. note::
    For source installations the `setuptools <https://github.com/pypa/setuptools>`_
    package is recommended.


Usage
-----

From command line::

  xmlschema-generator --help

From Python console or module::

  import xmlschema_generator as xg

or::

  from xmlschema_generator import generate

License
-------

This software is distributed under the terms of the BSD 3-Clause License.
See the file 'LICENSE' in the root directory of the present distribution,
or https://opensource.org/licenses/BSD-3-Clause.

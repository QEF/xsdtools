********
xsdtools
********

.. introduction-start

This package implements XSD schema-based code generators for Quantum ESPRESSO
simulation suite. The generator engine uses XSD schemas and Jinja2 templates
to produce code and structures.

The generator requires Python 3.7+ for working and is based on the libraries
`xmlschema <https://github.com/brunato/xmlschema>`_ and
`Jinja2 <https://github.com/pallets/jinja>`_.


Installation
============

First clone the project and then switch into its directory::

  git clone https://github.com/QEF/xsdtools.git
  cd xsdtools/

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

  xsdtools --help

From Python console or module::

  import xsdtools
  codegen = xsdtools.FortranGenerator('schema.xsd')
  codegen.render_to_files('*', output_dir='./output')

You can provide your own templates through *searchpath* argument::

  codegen = xsdtools.FortranGenerator('schema.xsd', searchpath='./templates')
  codegen.render_to_files('my_template.jinja', output_dir='./output')
    
Code generator classes
======================

* `xsdtools.CGenerator`
* `xsdtools.FortranGenerator`
* `xsdtools.QEFortranGenerator`

License
=======

This software is distributed under the terms of the BSD 3-Clause License.
See the file 'LICENSE' in the root directory of the present distribution,
or https://opensource.org/licenses/BSD-3-Clause.

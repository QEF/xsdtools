***************
Code generators
***************

Abstract base class
===================

Code generator classes have a common abstract base class that cannot be
used for generate code but defines a common API:

.. autoclass:: xmlschema_codegen.AbstractGenerator

    .. autoattribute:: xsd_file
    .. automethod:: register_filter
    .. automethod:: register_test
    .. automethod:: map_type
    .. automethod:: list_templates
    .. automethod:: matching_templates
    .. automethod:: get_template
    .. automethod:: select_template
    .. automethod:: render
    .. automethod:: render_to_files


Code generator classes
======================

.. autoclass:: xmlschema_codegen.CGenerator
.. autoclass:: xmlschema_codegen.PythonGenerator
.. autoclass:: xmlschema_codegen.FortranGenerator
.. autoclass:: xmlschema_codegen.QEFortranGenerator
.. autoclass:: xmlschema_codegen.JSONSchemaGenerator





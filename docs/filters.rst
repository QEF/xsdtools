****************
Template filters
****************

Within templates you can use a set of filters, available for all generator classes:

name
    Get the unqualified name of the object. Invalid
    chars for identifiers are replaced by an underscore.

qname
    Get the QName of the object in prefixed form. Invalid
    chars for identifiers are replaced by an underscore.

namespace
    Get the namespace URI associated to the object.

type_name
    Get the unqualified name of an XSD type. For default
    'Type' or '_type' suffixes are removed. Invalid
    chars for identifiers are replaced by an underscore.

type_qname
    Get the QName of an XSD type in prefixed form. For
    default 'Type' or '_type' suffixes are removed. Invalid
    chars for identifiers are replaced by an underscore.

sort_types
    Sort a sequence or a map of XSD types, in reverse
    dependency order, detecting circularities.


Type mapping
============

Each language base class has an additional filter for translating types using an
extendable map. For example :class:`FortranGenerator` has the filter *fortran_type*
and the :class:`CGenerator` has the filter *c_type*.

These filters are based on a common method *map_type* that uses the instance dictionary
called *types_map*, built at initialization time from a class maps for builtin types
and for schema types and an optional initialization argument.


Defining additional filters
===========================

Additional or overriding filters can be passed at instance creation using the argument
*filters*. If you want to derive a custom generator class you can provide your additional
filters also using class decorator function or decorating a method.

.. doctest::

    >>> from xmlschema_codegen import AbstractGenerator, filter_method
    >>>
    >>> class FooGenerator(AbstractGenerator):
    ...     formal_language = 'Foo'
    ...
    ...     @filter_method
    ...     def my_filter_method(self, obj):
    ...         """A method that filters an object using the schema."""
    ...
    ...     @staticmethod
    ...     @filter_method
    ...     def my_static_test_method(obj):
    ...         """A static method that filters an object."""
    ...
    >>>
    >>> @FooGenerator.register_filter
    ... def my_test_function(obj):
    ...     """A function that filters an object."""
    ...

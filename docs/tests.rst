**************
Template tests
**************

Within templates you can also use a set of tests, available for all generator classes:

derivation
    Test if an XSD type instance is a derivation of any of a list of
    other types. Other types are provided by qualified names.

extension
    Test if an XSD type instance is an extension of any of a list of
    other types. Other types are provided by qualified names.

restriction
    Test if an XSD type instance is a restriction of any of a list of
    other types. Other types are provided by qualified names.

multi_sequence
    Test if an XSD type is a complex type with complex content that at
    least one child can have multiple occurrences.


Defining additional tests
=========================

Additional or overriding template tests can be passed at instance creation using
the argument *tests*. Deriving a custom generator class you can provide additional
tests also using class decorator function or decorating a method.

.. doctest::

    >>> from xsdtools import AbstractGenerator, test_method
    >>>
    >>> class FooGenerator(AbstractGenerator):
    ...     formal_language = 'Foo'
    ...
    ...     @test_method
    ...     def my_test_method(self, obj):
    ...         """A method that returns True or False."""
    ...
    ...     @staticmethod
    ...     @test_method
    ...     def my_static_test_method(obj):
    ...         """A static method that returns True or False."""
    ...
    >>>
    >>> @FooGenerator.register_test
    ... def my_test_function(obj):
    ...     """A function that returns True or False."""
    ...


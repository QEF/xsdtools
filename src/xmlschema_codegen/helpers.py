#
# Copyright (c) 2020, Quantum Espresso Foundation and SISSA.
# Internazionale Superiore di Studi Avanzati). All rights reserved.
# This file is distributed under the terms of the BSD 3-Clause license.
# See the file 'LICENSE' in the root directory of the present distribution,
# or https://opensource.org/licenses/BSD-3-Clause
#
import re

XSD_NAMESPACE = "http://www.w3.org/2001/XMLSchema"

NAMESPACE_PATTERN = re.compile(r'{([^}]*)}')
NAME_PATTERN = re.compile(r'^(?:[^\d\W]|:)[\w.\-:]*$')
NCNAME_PATTERN = re.compile(r'^[^\d\W][\w.\-]*$')
QNAME_PATTERN = re.compile(
    r'^(?:(?P<prefix>[^\d\W][\w\-.\xb7\u0387\u06DD\u06DE]*):)?'
    r'(?P<local>[^\d\W][\w\-.\xb7\u0387\u06DD\u06DE]*)$',
)


def get_namespace(qname):
    if not qname or qname[0] != '{':
        return ''

    try:
        return NAMESPACE_PATTERN.match(qname).group(1)
    except (AttributeError, TypeError):
        return ''


def is_shell_wildcard(name):
    return '*' in name or '?' in name or '[' in name


def xsd_qname(name):
    return '{%s}%s' % (XSD_NAMESPACE, name)


def filter_method(func):
    """Marks a method for registration as template filter."""
    func.is_filter = True
    return func


def test_method(func):
    """Marks a method for registration as template test."""
    func.is_test = True
    return func

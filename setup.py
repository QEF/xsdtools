#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2020, SISSA (Scuola Internazionale Superiore di Studi Avanzati).
# All rights reserved.
# This file is distributed under the terms of the BSD 3-Clause license.
# See the file 'LICENSE' in the root directory of the present distribution,
# or https://opensource.org/licenses/BSD-3-Clause
#
try:
    from setuptools import setup
except ImportError:
    # noinspection PyUnresolvedReferences
    from distutils.core import setup

with open("README.rst") as readme:
    long_description = readme.read()

setup(
    name='xmlschema-generator',
    version='0.1',
    install_requires=['xmlschema>=1.1.0', 'jinja2'],
    packages=['xmlschema_generator'],
    package_data={'xmlschema_generator': ['templates/*/*.j2']},
    entry_points={
        'console_scripts': [
            'xmlschema-generate=xmlschema_generator.__main__:main',
        ]
    },
    author='Davide Brunato et al.',
    url='https://github.com/sissaschool/xmlschema-generator',
    license='BSD 3-Clause',
    description='A code generator based on XSD schemas and Jinja2 templates',
    long_description=long_description,
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Code Generators'
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
    ]
)

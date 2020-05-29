#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2020, SISSA (Scuola Internazionale Superiore di Studi Avanzati).
# All rights reserved.
# This file is distributed under the terms of the BSD 3-Clause license.
# See the file 'LICENSE' in the root directory of the present distribution,
# or https://opensource.org/licenses/BSD-3-Clause
#
from setuptools import find_packages, setup

with open("README.rst") as readme:
    long_description = readme.read()

setup(
    name='xmlschema-codegen',
    version='0.1',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'xmlschema-codegen=xmlschema_codegen.__main__:main',
        ]
    },
    install_requires=['xmlschema>=1.2.0', 'jinja2'],
    author='Davide Brunato et al.',
    url='https://github.com/sissaschool/xmlschema-codegen',
    license='BSD 3-Clause',
    license_file='LICENSE',
    description='A code generator for XSD schemas based on xmlschema and Jinja2 libraries',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Text Processing :: Markup :: XML',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
    ]
)

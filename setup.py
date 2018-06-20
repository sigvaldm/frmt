#!/usr/bin/env python
"""
Copyright 2018 Sigvald Marholm <marholm@marebakken.com>

This file is part of frmt.

frmt is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

frmt is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with frmt.  If not, see <http://www.gnu.org/licenses/>.
"""

from setuptools import setup

with open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

setup(name='frmt',
      version='1.1.0',
      description='Lightweight formatting of tables and times in Python',
      long_description=long_description,
      author='Sigvald Marholm',
      author_email='marholm@marebakken.com',
      url='https://github.com/sigvaldm/frmt.git',
      py_modules=['frmt'],
      license='LGPL'
     )


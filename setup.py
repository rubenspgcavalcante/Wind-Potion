#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License version 3 as
published by the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""
__author__ = "Rubens Pinheiro Gonçalves Cavalcante"
__date__ = "08/05/13 19:18"
__licence__ = "LGPLv3"
__email__ = "rubenspgcavalcante@gmail.com"

from setuptools import setup

setup(
    name='WindPotion',
    version='0.1',
    license="LGPLv3",
    description='A REST API for Tornado and SQLAlchemy Elixir',
    author='Rubens Pinheiro Gonçalves Cavalcante',
    author_email='rubenspgcavalcante@gmail.com',
    url="https://github.com/rubenspgcavalcante/Wind-Potion",
    download_url="https://github.com/rubenspgcavalcante/Wind-Potion/archive/master.zip",
    package_dir={'windpotion': 'src/windpotion'},
    packages=['windpotion'],
    install_requires=["Tornado", "SQLAlchemy", "Elixir"]
)

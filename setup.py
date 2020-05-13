'''ComputerRainbow - a toy program rendering rainbows at different resolutions
    Copyright (C) 2020  Bjoernar Tuftin

    This file is part of ComputerRainbow, a small PyQt based program.
    The program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.'''

    from setuptools import setup
    setup{
        name='ComputerRainbow',
        version='0.9',
        author='Bjoernar Tuftin',
        author_email='btuftin@gmail.com',
        description='a program for experimenting with rgb rainbows',
        url="https://github.com/btuftin/computer-rainbow",
        license='GPL v3',
        long_description=open('README.rst', 'r').read(),
        packages=['computerrainbow', 'computerrainbow.images'],
        install_requires=['PyQt5'],
        entry_points={
            'console_scripts': [
                'computerrainbow = computerrainbow.__main__:main'
            ]
        }
    }
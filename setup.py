#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This software is licensed as described in the README.rst and LICENSE
# files, which you should have received as part of this distribution.

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

DEPS = ['RPi.GPIO', 'requests']

CLASSIFIERS = [
    'Environment :: Console',
    'Intended Audience :: System Administrators',
    'Intended Audience :: Developers',
    'Operating System :: Unix',
    'Operating System :: POSIX :: Linux',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 3',
    'Development Status :: 3 - Alpha',
    'Topic :: Utilities'
]

with open("README.rst", "r") as fp:
    sensor_long_description = fp.read()

setup(
    name="RPi.Sensor",
    version="0.2.3a",
    author="Richard Kellner",
    author_email="richard.kellner@gmail.com",
    url="https://github.com/ricco386/rpi-sensor",
    description="Base class for Python objects for RPi sensors",
    long_description=sensor_long_description,
    license="MIT",
    py_modules=["sensor", "utils"],
    classifiers=CLASSIFIERS,
    install_requires=DEPS,
)

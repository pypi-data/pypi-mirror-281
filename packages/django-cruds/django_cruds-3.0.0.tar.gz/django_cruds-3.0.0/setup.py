#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import cruds

from setuptools import setup

version = cruds.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.md').read()

setup(
    name='django-cruds',
    version=version,
    description="""django-cruds is simple drop-in django app that creates CRUD for faster prototyping.""",  # noqa
    long_description=readme,
    author='Bojan Mihelac',
    author_email='bmihelac@mihelac.org',
    url='https://github.com/bmihelac/django-cruds',
    packages=[
        'cruds',
    ],
    include_package_data=True,
    install_requires=[
        'Django>=4.2,<5',
    ],
    license="BSD",
    zip_safe=False,
    keywords='django-cruds',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)

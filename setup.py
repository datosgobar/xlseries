#!/usr/bin/env python
# -*- coding: utf-8 -*-


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.md') as readme_file:
    readme = readme_file.read()

with open("requirements.txt") as f:
    requirements = [req.strip() for req in f.readlines()]

test_requirements = [
    "nosetests",
    "coverage"
]

setup(
    name='xlseries',
    version='0.1.0',
    description="Python package to scrape data series from excel files.",
    long_description=readme,
    author="Agustin Benassi",
    author_email='agusbenassi@gmail.com',
    url='https://github.com/abenassi/xlseries',
    packages=[
        'xlseries',
    ],
    package_dir={'xlseries':
                 'xlseries'},
    include_package_data=True,
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
    keywords='xlseries',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7'
    ],
    test_suite='nosetests',
    tests_require=test_requirements
)

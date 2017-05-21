# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

setup(
    name='yhashmap',
    version='0.1.0',
    description='hashmap implementation',
    long_description=readme,
    author='Joseph DeVita',
    author_email='jodvita@gmail.com',
    url='https://github.com/v1ta/yhashmap',
    license=license,
    packages=find_packages(exclude=('tests', 'bin', 'include'))
)

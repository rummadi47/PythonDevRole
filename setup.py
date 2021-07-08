#!/usr/bin/env python3
import pathlib
import pkg_resources
from setuptools import setup

with pathlib.Path('requirements.txt').open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]
setup(name='Distutils',
      version='1.0',
      description='Python Distribution Utilities',
      author='Saritha Ummadi',
      install_requires=install_requires,
      author_email='post.saritha2154@gmail.com',
      url='https://www.python.org/sigs/distutils-sig/',
      packages=['distutils', 'distutils.command'],
     )


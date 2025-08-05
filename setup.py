import os
import sys
import shutil
from setuptools import setup, find_packages, find_namespace_packages
from setuptools.command.install import install

setup(name='randomspanish',
      version='1.0.0',
      description='Spanish learning app',
      author='David Nidever',
      author_email='dnidever@montana.edu',
      url='https://github.com/dnidever/randomspanish',
      requires=['numpy','dlnpyutils'],
      zip_safe = False,
      include_package_data=True,
      packages=find_namespace_packages(where="python"),
      package_dir={"": "python"}      
)

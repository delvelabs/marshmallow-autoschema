#!/usr/bin/env python

from setuptools import setup

version_file = "marshmallow_autoschema/__version__.py"
version_data = {}
with open(version_file) as f:
    code = compile(f.read(), version_file, 'exec')
    exec(code, globals(), version_data)

setup(name='marshmallow-autoschema',
      version=version_data['__version__'],
      description='Generate marshmallow schemas from type annotations and decorators.',
      author='Delve Labs inc.',
      author_email='info@delvelabs.ca',
      url='https://github.com/delvelabs/marshmallow-autoschema',
      packages=['marshmallow_autoschema'],
      install_requires=[
          'marshmallow',
      ],
      license="MIT")

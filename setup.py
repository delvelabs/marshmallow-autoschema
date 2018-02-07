#!/usr/bin/env python

import os
from setuptools import setup


version_file = "marshmallow_autoschema/__version__.py"
version_data = {}
with open(version_file) as f:
    code = compile(f.read(), version_file, 'exec')
    exec(code, globals(), version_data)


def dep_list(filename):
    out = []

    path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(path, filename)) as fp:
        for line in fp:
            clean = line.strip()
            if clean:
                out.append(clean)

    return out


setup(name='marshmallow-autoschema',
      version=version_data['__version__'],
      description='Generate marshmallow schemas from type annotations and '
                  'decorators.',
      author='Delve Labs inc.',
      author_email='info@delvelabs.ca',
      url='https://github.com/delvelabs/marshmallow-autoschema',
      packages=['marshmallow_autoschema'],
      install_requires=dep_list("requirements.txt"),
      license="MIT")

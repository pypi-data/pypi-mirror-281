# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rpmautospec_core']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'rpmautospec-core',
    'version': '0.1.5',
    'description': 'Core functionality for rpmautospec',
    'long_description': 'This package contains core functionality for rpmautospec.\n\nThis code shall have no external dependencies beyond what is contained in the Python standard\nlibrary.\n',
    'author': 'Nils Philippsen',
    'author_email': 'nils@redhat.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/fedora-infra/rpmautospec-core',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

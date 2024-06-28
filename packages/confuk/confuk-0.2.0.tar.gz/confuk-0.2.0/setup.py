# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['confuk']

package_data = \
{'': ['*']}

install_requires = \
['easydict>=1.11,<2.0', 'pydantic>=2.5.3,<3.0.0', 'toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'confuk',
    'version': '0.2.0',
    'description': 'Very opinionated configuration loading package for Python projects',
    'long_description': '# Confuk\n\nThis is yet another package for managing configuration files in Python projects.\n\nAt the moment all it does is it exposes a consistent API that lets you provide a path to a TOML configuration file. It parses the config file into a dictionary by default. If a config class is provided when parsing, the class instance will be created using a dictionary of keyword arguments coming from the original TOML file.\n\nIn human words: I made this package so that I don\'t have to explicilty load, parse and return a class instance every single time I have something to do with a TOML file:\n\n```python\nfrom confuk import parse_config\nfrom pathlib import Path\nfrom somewhere import ConfigClass\n\ncfg_dict = parse_config(Path("some.toml"))  # returns a dictionary\ncfg_obj = parse_config(Path("some.toml"), ConfigClass)  # returns an instance of `ConfigClass`\n```\n\n## Installation\n\nCurrently you can build the package using Poetry:\n\n1. Clone this repo.\n2. Run `poetry build`.\n3. Grab the installable wheel from the `dist` folder and install it with `pip` or add the package as a local dependency of another project.\n\nOnce I get some time to take care of it I will add the package to PyPI so that it\'s installable via a simple `pip install confuk` command.\n',
    'author': 'Krzysztof J. Czarnecki',
    'author_email': 'kjczarne@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)

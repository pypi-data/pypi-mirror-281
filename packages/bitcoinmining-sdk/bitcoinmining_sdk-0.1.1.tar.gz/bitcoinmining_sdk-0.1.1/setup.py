# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bitcoinmining_sdk']

package_data = \
{'': ['*']}

install_requires = \
['tuyul-online-sdk>=0.0.8,<0.0.9']

setup_kwargs = {
    'name': 'bitcoinmining-sdk',
    'version': '0.1.1',
    'description': '',
    'long_description': 'Support Termux and Windows\n\nWindows - Python version 3.8+\nTermux - Python version 3.11+\n\n\nInstall in Termux\n\npkg update\n\npkg upgrade\n\npkg install x11-repo && apt update\n\npkg install opencv rust python-cryptography python-numpy python-lxml binutils-is-llvm\n\naarch64-linux-android-ar\n\npython -m pip install bitcoinmining-sdk\n\nor\n\npip install bitcoinmining-sdk',
    'author': 'DesKaOne',
    'author_email': 'DesKaOne@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

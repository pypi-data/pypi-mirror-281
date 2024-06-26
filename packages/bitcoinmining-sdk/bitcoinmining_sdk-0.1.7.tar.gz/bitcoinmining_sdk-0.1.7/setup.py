# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bitcoinmining_sdk']

package_data = \
{'': ['*']}

install_requires = \
['tuyul-online-sdk>=0.1.1,<0.2.0']

setup_kwargs = {
    'name': 'bitcoinmining-sdk',
    'version': '0.1.7',
    'description': '',
    'long_description': "\n# BitcoinMining-SDK\nSupport Termux and Windows\n## Environment Variables\n\nTo run this project, you will need to add the following environment variables to your .env file\n\n`API_KEY`\n\n`ADDRESS`\n\n`KODE_REFERRAL`\n\n\n## Install in Termux\n\n```bash\n    pkg update\n\n    pkg upgrade\n\n    pkg install x11-repo\n\n    pkg install opencv\n\n    pkg install rust\n\n    pkg install python-cryptography\n\n    pkg install python-numpy\n\n    pkg install lxml\n\n    pkg install binutils-is-llvm\n\n    aarch64-linux-android-ar\n\n    python -m pip install -U bitcoinmining-sdk\n\n    or\n\n    pip install -U bitcoinmining-sdk\n```\n    \n## Usage/Examples\ncreate main.py\n```python\nfrom dotenv import load_dotenv\nload_dotenv()\nfrom bitcoinmining_sdk import Worker, Start\n\n\nif __name__ == '__main__':\n    Worker.run(Start)\n```\n\n\n## Running Tests\n\nTo run tests, run the following command\n\n```python\n  python main.py\n```",
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

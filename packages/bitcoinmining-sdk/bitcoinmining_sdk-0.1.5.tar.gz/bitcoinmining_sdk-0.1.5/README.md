
# BitcoinMining-SDK
Support Termux and Windows
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`API_KEY`

`ADDRESS`

`KODE_REFERRAL`


## Install in Termux

```bash
    pkg update

    pkg upgrade

    pkg install x11-repo

    pkg install opencv

    pkg install rust

    pkg install python-cryptography

    pkg install python-numpy

    pkg install lxml

    pkg install binutils-is-llvm

    aarch64-linux-android-ar

    python -m pip install -U bitcoinmining-sdk

    or

    pip install -U bitcoinmining-sdk
```
    
## Usage/Examples
create main.py
```python
from dotenv import load_dotenv
load_dotenv()
from bitcoinmining_sdk import Worker, Start


if __name__ == '__main__':
    Worker.run(Start)
```


## Running Tests

To run tests, run the following command

```python
  python main.py
```
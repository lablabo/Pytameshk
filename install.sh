#!/usr/bin/env bash
sudo python3 system/helper/pip/get-pip.py
sudo python3 -m pip --version
sudo python3 -m pip install flash
sudo python3 -m pip install uuid
sudo python3 -m pip install platform
sudo python3-m pip install numpy
sudo python3 -m pip install socket
sudo python3 -m pip install itertools
sudo python3 -m pip install re
sudo python3 -m pip install requests
sudo python3 -m pip install cryptography

print "------ Installer Ended ------"
sudo python index.py

#!/usr/bin/env bash
# Installs dev environment
sudo python3 -m pip install --upgrade pip setuptools wheel tqdm
python3 -m pip install --user --upgrade twine
sudo python3 -m pip install -r requirements.txt
cp .pypirc ~
echo
echo "Do not forget to enter password to ~/.pypirc"
echo

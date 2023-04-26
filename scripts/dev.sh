#!/usr/bin/env bash
# Installs dev environment
python -m pip install --upgrade pip setuptools wheel tqdm
python -m pip install --user --upgrade twine
python -m pip install -r requirements.txt
cp .pypirc ~
echo
echo "Do not forget to enter password to ~/.pypirc"
echo

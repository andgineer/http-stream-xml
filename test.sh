#!/usr/bin/env bash
#
# Run all tests
# To filter by test name use test.sh -k <pattern or substring>
#
RED='\033[1;31m'
GREEN='\033[1;32m'
CYAN='\033[1;36m'
NC='\033[0m' # No Color
NL=$'\n'

python -m unittest discover --start-directory tests --verbose $@

if [ $? -eq 0 ]; then
  echo
  echo -e $GREEN"success!"$NC
else
  echo
  echo -e $RED"fail"$NC
fi
echo

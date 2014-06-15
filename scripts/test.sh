#!/bin/bash

find . -not -path "./.git"

echo "##############"
echo "# unit tests #"
echo "##############"

python utils/sims.py || exit 1
python utils/stepvals.py || exit 1

echo "#################"
echo "# pylint report #"
echo "#################"

pylint utils *.py

exit 0

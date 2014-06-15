#!/bin/bash

ls -aR ./

echo "##############"
echo "# unit tests #"
echo "##############"

python -m unittest utils.test_sims || exit 1

echo "#################"
echo "# pylint report #"
echo "#################"

pylint utils *.py

exit 0

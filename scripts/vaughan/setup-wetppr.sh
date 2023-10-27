#!/bin/bash
# Prepare the remote environment for wetppr exercises.
# This script accepts the same arguments as env-lmod.sh

# Debug this script ------------------------------------------------------------
# set -eux

# Retrieve the parent directory of this script
my_app_path=$(dirname $(readlink -f "$0"))

# fix the "vscode fails to connect due to file quota exceeded." issue:
${my_app_path}/../mv.vscode-server.sh

# Load LMOD modules 
source ${my_app_path}/env-lmod.sh $@
ml
echo

# install wiptools
pip install --user wiptools
pip install --user nanobind
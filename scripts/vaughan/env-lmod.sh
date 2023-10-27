#!/bin/bash
# call this script as
#   > source path/to/wetppr/scripts/vaughan/env-lmod.sh [foss[/toolchain_version]]
# to load the foss toolchain_name, or 
#   > source path/to/wetppr/scripts/vaughan/env-lmod.sh intel[/toolchain_version]
# to load the intel toolchain_name.

# Debug this script ------------------------------------------------------------
# set -eux

# Functions --------------------------------------------------------------------
usage()
{
    echo "Load usefull modules from a given toolchain (default is ${default_toolchain_name}/${default_toolchain_version})"
    echo "Usage: "
    echo "  $0 -h : help"
    echo "  $0 [toolchain_name[/toolchain_version]]"
    exit 2
}

ml_verbose()
{
    echo "module load $1"
    ml $1
}

# Set default values -----------------------------------------------------------
default_toolchain_name=foss
default_toolchain_version=2022a

# Handle command line arguments ------------------------------------------------
while getopts "vh" opt; do
  case $opt in
    h)  
        echo "usage"
        usage
        ;;
  esac
done
shift $((OPTIND-1))
if [ $@ ]
then
    supplied_toolchain=$1
    # Did the user also supply also supply a toolchain version
    supplied_toolchain_version=$(basename ${supplied_toolchain})
    if [ "${supplied_toolchain_version}" = "${supplied_toolchain}" ]
    then # no toolchain version supplied, only the toolchain name
        toolchain_name=${supplied_toolchain}
        toolchain_version=${default_toolchain_version}
    else # both toolchain name and version supplied
        toolchain_name=$(dirname ${supplied_toolchain})
        toolchain_version=${supplied_toolchain_version}
    fi
else # nothing provided
    toolchain_name=${default_toolchain_name}
    toolchain_version=${default_toolchain_version}
fi

echo
echo "Using toolchain_name ${toolchain_name}/${toolchain_version} "
echo

# Set LMOD environmemt ---------------------------------------------------------
module --force purge

ml_verbose calcua/${toolchain_version}
ml_verbose $toolchain_name
ml_verbose SciPy-bundle
ml_verbose numba
echo "wip-tools dependencies:"
ml_verbose CMake
ml_verbose git
ml_verbose gh
echo

# Allow to pip install missing python packages yourself ------------------------
# If $PYTHONUSERBASE is already set, it is kept as is.
# Otherwise, it is set to ${VSC_DATA}/.local.
if [ -z "$PYTHONUSERBASE" ]
then
    export PYTHONUSERBASE=${VSC_DATA}/.local
fi
# Make sure the folder exists:
mkdir -p ${PYTHONUSERBASE}
# check if $PATH has ${PYTHONUSERBASE}/bin
if [[ ":$PATH:" == *":${PYTHONUSERBASE}/bin:"* ]]
then
    : # PATH is correctly set
else
    export PATH="$PATH:${PYTHONUSERBASE}/bin"
fi
# ------------------------------------------------------------------------------
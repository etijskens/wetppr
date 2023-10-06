#!/bin/bash

if [ "$1" = "" ]
then 
    echo "ERROR: toolchain not provided: [foss|intel]" 1>&2
    return 1
fi

export toolchain_version=2022a

export toolchain=$1

module --force purge
ml calcua/${toolchain_version}
ml $toolchain
ml SciPy-bundle
ml CMake
ml
echo
echo "Using toolchain ${toolchain}/${toolchain_version} "
echo
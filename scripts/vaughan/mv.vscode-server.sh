#!/bin/bash
# Run this script to move the .vscode-server directory to $VSC_DATA 
# to avoid `file quota exceeded` errors on $VSC_HOME.
set -eux

cd $VSC_HOME
if [ -d .vscode-server ]
    # directory $VSC_HOME/.vscode-server exists
then
    if [ -L .vscode-server]
    then 
        # but it is a soft link
        echo "There is already a soft link for .vscode-server"
        exit 0
    else
        mv .vscode-server $VSC_DATA/
        echo "Moved .vscode-server to $VSC_DATA."
    fi
else
    mkdir -p $VSC_DATA/.vscode-server
    echo "Created directory $VSC_DATA/.vscode-server."
fi

ln -s $VSC_DATA/.vscode-server
echo "Created soft link to $VSC_DATA/.vscode-server in $VSC_HOME."

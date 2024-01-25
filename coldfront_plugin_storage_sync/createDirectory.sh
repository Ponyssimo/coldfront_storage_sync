#!/bin/bash

# script is based off of instructions in https://kgcoe-git.rit.edu/research-computing/docs/-/wikis/shared_user_space
# needs the CLAWS group and autofs file changes made before running

# First argument is the name of the project
# Second argument is the size being allocated in bytes
PROJECT=$1
SIZE=$2
if [ -z $PROJECT ]; then
    exit 1
fi
if [ -z $SIZE ]; then
    exit 2
fi

# Create new directory if it doesn't exist
if [ ! -d /cephfs/rc/shared/$PROJECT ]; then
    # assuming the directory name matches the project name
    mkdir /cephfs/rc/shared/rc/$PROJECT
    mkdir /cephfs/rc/home/rc/$PROJECT

    # this might have to be changed to include the full path
    # assuming group name matches the project name
    chgrp $PROJECT $PROJECT
    chmod 2770 $PROJECT
    setfacl -R -m default:group:$PROJECT:rwx sharepath
fi
setfattr -n ceph.quota.max_bytes -v SIZE $PROJECT

df $PROJECT

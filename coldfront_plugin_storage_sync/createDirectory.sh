#!/bin/bash

# script is based off of instructions in https://kgcoe-git.rit.edu/research-computing/docs/-/wikis/shared_user_space
# needs the CLAWS group and autofs file changes made before running

PROJECT=$1
if [ -z $PROJECT ]
then
    exit 1
fi

# assuming the directory name matches the project name
mkdir /cephfs/rc/shared/rc/$PROJECT
mkdir /cephfs/rc/home/rc/$PROJECT

# this might have to be changed to include the full path
# assuming group name matches the project name
chgrp $PROJECT $PROJECT
chmod 2770 $PROJECT
setfacl -R -m default:group:$PROJECT:rwx sharepath
setfattr -n ceph.quota.max_bytes -v 1099511627776 $PROJECT

df $PROJECT

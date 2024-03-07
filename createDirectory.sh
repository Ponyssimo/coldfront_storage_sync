#!/bin/bash

# script is based off of instructions in https://kgcoe-git.rit.edu/research-computing/docs/-/wikis/shared_user_space
# needs the CLAWS group and autofs file changes made before running

# First argument is the name of the project
# Second argument is the size being allocated in bytes
PROJECT=$1
SIZE=$2

# exit if no name give
if [ -z $PROJECT ]; then
    exit 1
fi

# exit if no size given
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
    chgrp $PROJECT /cephfs/rc/shared/rc/$PROJECT
    chmod 2770 /cephfs/rc/shared/rc/$PROJECT
    setfacl -R -m default:group:$PROJECT:rwx sharepath

    # making changes in gitlab
    # need to figure out working directory maybe
    git pull
    echo '-fstype=ceph,name=shared_rc,secretfile=/etc/ceph/ceph.shared_rc.secret,nosuid,_netdev,rbytes ceph-mdss.rc.rit.edu:/shared/rc/${PROJECT}' >> auto.shared.rc # this probably isn't right
    git add auto.shared.rc
    git commit -m 'added ${PROJECT} to auto.shared.rc'
    git push
else
    CURRENT=${getfattr -n ceph.quota.max_bytes $PROJECT}
    if [ SIZE == CURRENT ]; then
        exit 3
    fi
fi
setfattr -n ceph.quota.max_bytes -v $SIZE /cephfs/rc/shared/rc/$PROJECT

df $PROJECT

exit 0

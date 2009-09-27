#!/bin/sh

REMOTE_HOST=$1
if [[ "$REMOTE_HOST" == "" ]] ; then
    echo "You must provide the remote host as a parameter to the script."
    exit
fi
PUB_KEY=~/.ssh/id_rsa.pub
if [ ! -f $PUB_KEY ]; then
    ssh-keygen -t rsa
fi
ssh $REMOTE_HOST \
    "mkdir .ssh && chmod 700 .ssh || echo '.ssh directory already exists; skipping creation...'"
scp $PUB_KEY $REMOTE_HOST:.ssh/authorized_keys2_tmp
ssh $REMOTE_HOST \
    "cat .ssh/authorized_keys2_tmp >> .ssh/authorized_keys2; rm .ssh/authorized_keys2_tmp;chmod 700 .ssh/authorized_keys2"


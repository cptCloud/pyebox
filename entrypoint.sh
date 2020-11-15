#!/bin/sh
set -e

# Check user and password
if [ -z "$PYEBOX_MYACCOUNT" ] || [ -z "$PYEBOX_MYPASSWORD" ]
then
    echo 'Error: No user or password. Set both environnement variables PYEBOX_MYACCOUNT and PYEBOX_MYPASSWORD'
    exit 1
else
    pyebox -u $PYEBOX_MYACCOUNT -p $PYEBOX_MYPASSWORD
fi

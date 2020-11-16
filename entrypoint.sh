#!/bin/sh
set -e

# Check user and password
if [ -z "$PYEBOX_MYACCOUNT" ] || [ -z "$PYEBOX_MYPASSWORD" ] && [ "$PYEBOX_OUTPUT" != "MQTT" ]
then
    echo 'Error: No user or password. Set both environnement variables PYEBOX_MYACCOUNT and PYEBOX_MYPASSWORD or PYEBOX_OUTPUT=MQTT'
    exit 1
fi

# Config
if [ -z "$CONFIG" ]
then
    export CONFIG="/usr/src/app/config.yaml"
fi

if [ "$PYEBOX_OUTPUT" == "MQTT" ]
then
    mqtt_pyebox
else
    pyebox -u $PYEBOX_MYACCOUNT -p $PYEBOX_MYPASSWORD
fi


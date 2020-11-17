######
PyEbox
######

TODO
####

* Add non offpeak account support

Installation
############

::

    pip install pyebox


Usage
#####

Print your current data

::

    pyebox -u MYACCOUNT -p MYPASSWORD


Print help

::

    pyebox -h
    usage: pyebox [-h] -u USERNAME -p PASSWORD [-j] [-t TIMEOUT]

    optional arguments:
      -h, --help            show this help message and exit
      -u USERNAME, --username USERNAME
                            EBox account
      -p PASSWORD, --password PASSWORD
                            Password
      -j, --json            Json output
      -t TIMEOUT, --timeout TIMEOUT
                            Request timeout
                            
MQTT_deamon
#######
::
cp config.yaml.sample config.yaml
::
docker run -e PYEBOX_MYACCOUNT=*** -e PYEBOX_MYPASSWORD=*** -e PYEBOX_OUTPUT=MQTT -e MQTT_USERNAME=mqtt_username -e MQTT_PASSWORD=mqtt_password -e MQTT_HOST=mqtt_ip -e MQTT_PORT=mqtt_port -e ROOT_TOPIC=homeassistant -e MQTT_NAME=ebox pyebox
    
Docker
#######
::
docker build -t pyebox .
::
docker run -e PYEBOX_MYACCOUNT=*** -e PYEBOX_MYPASSWORD=*** pyebox

Dev env
#######

::

    virtualenv -p /usr/bin/python3.5 env
    pip install -r requirements.txt 

Upload Pypi Package
###################

::

    python setup.py sdist upload -r pypi

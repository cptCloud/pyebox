"""MQTT Daemon which collected Ebox Data.
And send it to MQTT using Home-Assistant format.
"""
import asyncio
import json
import os
import uuid

from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader
import mqtt_hass_base

from pyebox.client import EboxClient, USAGE_MAP

def get_mac():
    """Get mac address."""
    mac_addr = (':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                for ele in range(0, 8 * 6, 8)][::-1]))
    return mac_addr


class MqttEbox(mqtt_hass_base.MqttDevice):
    """MQTT MqttEbox."""

    timeout = None
    frequency = None

    def __init__(self):
        """Create new MqttEbox Object."""
        mqtt_hass_base.MqttDevice.__init__(self, "mqtt-ebox")

    def read_config(self):
        """Read config from yaml file."""
        with open(os.environ['CONFIG']) as fhc:
            self.config = load(fhc, Loader=Loader)
        self.timeout = self.config.get('timeout', 30)
        # 6 hours
        self.frequency = self.config.get('frequency', None)

    async def _init_main_loop(self):
        """Init before starting main loop."""

    def _publish_sensor(self, sensor_type, contract_id,
                        unit=None, device_class=None, icon=None):
        """Publish a Home-Assistant MQTT sensor."""
        mac_addr = get_mac()

        base_topic = ("{}/sensor/ebox_{}".format(self.mqtt_root_topic,
                                                        contract_id))

        sensor_config = {}
        sensor_config["device"] = {"connections": [["mac", mac_addr]],
                                   "name": "ebox_{}".format(contract_id),
                                   "identifiers": ['ebox', contract_id],
                                   "manufacturer": "mqtt-ebox",
                                   "sw_version": "0"}

        sensor_state_config = "{}/{}/state".format(base_topic, sensor_type)
        sensor_config.update({
            "state_topic": sensor_state_config,
            "name": "ebox_{}_{}".format(contract_id, sensor_type),
            "unique_id": "{}_{}".format(contract_id, sensor_type),
            "force_update": True,
            "expire_after": 0,
            })

        sensor_config_topic = "{}/{}/config".format(base_topic, sensor_type)

        self.mqtt_client.publish(topic=sensor_config_topic,
                                 retain=True,
                                 payload=json.dumps(sensor_config))

        return sensor_state_config

    async def _main_loop(self):
        """Run main loop."""
        self.logger.debug("Get Data")
        for account in self.config['accounts']:
            client = EboxClient(account['username'],
                                       account['password'],
                                       self.timeout)
            await client.fetch_data()
            fetched_data = client.get_data()

            # Balance
            # Publish sensor
            balance_topic = self._publish_sensor('balance', account['username'],
                                                    unit="$", device_class=None,
                                                    icon="mdi:currency-usd")
            # Send sensor data
            self.mqtt_client.publish(
                    topic=balance_topic,
                    payload=fetched_data['balance'])

            # Usage
            # Publish sensor
            usage_topic = self._publish_sensor('usage', account['username'],
                                                    unit="%", device_class=None,
                                                    icon="mdi:currency-usd")
            # Send sensor data
            self.mqtt_client.publish(
                    topic=usage_topic,
                    payload=fetched_data['usage'])

            # Before offpeak and offpeak data
            for data_name in USAGE_MAP.items():
                # Publish sensor
                sensor_topic = self._publish_sensor(data_name,
                                                    account['username'],
                                                    unit='Gb',
                                                    icon=None,
                                                    device_class=None)
                # Send sensor data
                self.mqtt_client.publish(
                        topic=sensor_topic,
                        payload=fetched_data[data_name])

            await client.close_session()

        if self.frequency is None:
            self.logger.info("Frequency is None, so it's a one shot run")
            self.must_run = False
            return

        self.logger.info("Waiting for %d seconds before the next check", self.frequency)
        i = 0
        while i < self.frequency and self.must_run:
            await asyncio.sleep(1)
            i += 1

    def _on_connect(self, client, userdata, flags, rc):
        """On connect callback method."""

    def _on_publish(self, client, userdata, mid):
        """MQTT on publish callback."""

    def _mqtt_subscribe(self, client, userdata, flags, rc):
        """Subscribe to all needed MQTT topic."""

    def _on_message(self, client, userdata, msg):
        """MQTT on message callback."""

    def _signal_handler(self, signal_, frame):
        """Handle SIGKILL."""

    async def _loop_stopped(self):
        """Run after the end of the main loop."""
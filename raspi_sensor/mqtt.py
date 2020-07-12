#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This software is licensed as described in the README.rst and LICENSE files,
# which you should have received as part of this distribution.
import paho.mqtt.client as mqtt

from .sensor import Sensor
from .exceptions import ConfigError


class MqttSensor(Sensor):
    client = None
    topic = ''
    broker_url = ''
    broker_port = 1883
    broker_keepalive = 5

    def __init__(self, name='Sensor', params=()):
        super().__init__(name=name, params=params)

        if 'mqtt' not in self.config:
            raise ConfigError('Missing "mqtt" section in config file.')

        self.broker_url = self.config.get('mqtt', 'broker_url', fallback=self.broker_url)
        self.broker_port = int(self.config.get('mqtt', 'broker_port', fallback=self.broker_port))

        self.client = mqtt.Client()

        self.logger.debug('MQTT is_connected %s:', self.client.is_connected())
        self.logger.debug('MQTT state %s:', self.client._state)

        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.enable_logger(self.logger)

        if self.config['mqtt']['broker_username'] and self.config['mqtt']['broker_password']:
            self.client.username_pw_set(username=self.config['mqtt']['broker_username'],
                                        password=self.config['mqtt']['broker_password'])

        if self.NAME in self.config:
            self.topic = self.config.get(self.NAME, 'mqtt_topic', fallback=None)
            self.logger.debug('Sensor %s MQTT topic set to: %s', self.NAME, self.topic)

        self.connect()

    def setup_args(self, params):
        super().setup_args(params=params)

        if hasattr(params, 'topic') and params.topic:
            self.topic = params.topic
            self.logger.debug('Sensor %s at topic: %s (set by script parameter).', self.NAME, self.topic)
        elif self.topic is None:
            raise ConfigError('Missing MQTT topic.')

    @staticmethod
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            client.client._easy_log(mqtt.MQTT_LOG_INFO, "Successfully connected to broker")
        elif rc == 1:
            raise RuntimeError("Connection failed: incorrect protocol version")
        elif rc == 2:
            raise RuntimeError("Connection failed: invalid client identifier")
        elif rc == 3:
            raise RuntimeError("Connection failed: server unavailable")
        elif rc == 4:
            raise RuntimeError("Connection failed: bad app_id or access_key")
        elif rc == 5:
            raise RuntimeError("Connection failed: not authorised")
        else:
            raise RuntimeError("Connection failed: returned code=", rc)

    @staticmethod
    def on_disconnect(client, userdata, rc):
        if rc == 0:
            client._easy_log(mqtt.MQTT_LOG_INFO, "Successfully disconnected from broker")
        else:
            client._easy_log(mqtt.MQTT_LOG_ERROR, "Broker disconnected failed: returned code=%s", rc)

    def connect(self):
        if self.client._state == mqtt.mqtt_cs_new:
            self.logger.debug('Sensor %s connecting to MQTT broker %s:%s', self.NAME, self.broker_url, self.broker_port)

            try:
                self.client.connect(self.broker_url, self.broker_port, keepalive=self.broker_keepalive)
            except RuntimeError as e:
                self.client._easy_log(mqtt.MQTT_LOG_ERROR, 'MQTT error - %s', e)

            self.publish_availability()

    def reconnect(self):
        if not self.client.is_connected():
            try:
                self.client.reconnect()
            except RuntimeError as e:
                self.client._easy_log(mqtt.MQTT_LOG_ERROR, 'MQTT error - %s', e)

            # self.publish_availability()

    def publish(self, topic=None, payload=None):
        if topic is None:
            topic = self.topic

        # self.reconnect()

        return self.client.publish(topic=topic, payload=payload, qos=1, retain=False)

    def publish_availability(self, available=True):
        if available:
            payload = 1
        else:
            payload = 0

        return self.publish(topic=f'{self.topic}/availability', payload=payload)

    def exit_callback(self):
        super().exit_callback()
        self.publish_availability(available=False)
        self.client.disconnect()

    def failed_notification_callback(self):
        super().failed_notification_callback()
        self.publish_availability(available=False)

    def post_sensor_read_callback(self):
        super().post_sensor_read_callback()

        if self.FAILED == 0:
            self.publish_availability(available=True)

    def notify(self, topic=None, payload=None):
        super().notify(topic=topic, payload=payload)
        self.publish(topic=topic, payload=payload)

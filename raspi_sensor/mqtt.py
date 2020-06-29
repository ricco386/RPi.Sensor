#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This software is licensed as described in the README.rst and LICENSE files,
# which you should have received as part of this distribution.
import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client._easy_log(mqtt.MQTT_LOG_INFO, "Successfully connected to broker")
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


def on_disconnect(client, userdata, rc):
    if rc == 0:
        client._easy_log(mqtt.MQTT_LOG_INFO, "Successfully disconnected from broker")
    else:
        client._easy_log(mqtt.MQTT_LOG_ERROR, "Broker disconnected failed: returned code=%s", rc)


def mqtt_init_client(config, logger=None):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect

    if logger:
        client.enable_logger(logger)

    if config['mqtt']['broker_username'] and config['mqtt']['broker_password']:
        client.username_pw_set(username=config['mqtt']['broker_username'], password=config['mqtt']['broker_password'])

    return client


def mqtt_connect(client, config):
    try:
        if client._state == mqtt.mqtt_cs_new:
            client.connect(config['mqtt']['broker_url'], int(config['mqtt']['broker_port']),
                           keepalive=config.get('mqtt', 'broker_keepalive', fallback=60))
        elif not client.is_connected():
            client.reconnect()

    except RuntimeError as e:
        client._easy_log(mqtt.MQTT_LOG_ERROR, 'MQTT error - %s', e)

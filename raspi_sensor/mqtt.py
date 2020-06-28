#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This software is licensed as described in the README.rst and LICENSE files,
# which you should have received as part of this distribution.
import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True
    elif rc == 1:
        raise RuntimeError("connection failed: incorrect protocol version")
    elif rc == 2:
        raise RuntimeError("connection failed: invalid client identifier")
    elif rc == 3:
        raise RuntimeError("connection failed: server unavailable")
    elif rc == 4:
        raise RuntimeError("connection failed: bad app_id or access_key")
    elif rc == 5:
        raise RuntimeError("connection failed: not authorised")
    else:
        raise RuntimeError("connection failed: returned code=", rc)


def init_mqtt_client(config, logger=None):
    client = mqtt.Client()
    client.on_connect = on_connect

    if logger:
        client.enable_logger(logger)

    if config['mqtt']['broker_username'] and config['mqtt']['broker_password']:
        client.username_pw_set(username=config['mqtt']['broker_username'], password=config['mqtt']['broker_password'])

    return client

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This software is licensed as described in the README.rst and LICENSE files,
# which you should have received as part of this distribution.
import paho.mqtt.client as mqtt


def init_mqtt_client(config):
    if 'mqtt' in config:
        client = mqtt.Client()

        if config['mqtt']['broker_username'] and config['mqtt']['broker_password']:
            client.username_pw_set(username=config['mqtt']['broker_username'],
                                   password=config['mqtt']['broker_password'])

        client.connect(config['mqtt']['broker_url'], int(config['mqtt']['broker_port']))
    else:
        client = None

    return client

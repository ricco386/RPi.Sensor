#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This software is licensed as described in the README.rst and LICENSE files,
# which you should have received as part of this distribution.
import os
import sys
import logging
import subprocess
import paho.mqtt.client as mqtt

from configparser import ConfigParser

LOG_LEVELS = frozenset(['DEBUG', 'INFO', 'WARN', 'WARNING', 'ERROR', 'FATAL', 'CRITICAL'])


def init_config_file():
    """
    Load configuration file and search in different locations.
    """
    cfg = 'sensor.cfg'
    cfg_fp = None
    cfg_lo = ((os.path.expanduser('~'), '.' + cfg), (sys.prefix, 'etc', cfg), ('/etc', cfg))

    # Try to read config file from ~/.sensor.cfg or /etc/sensor.cfg
    for i in cfg_lo:
        try:
            cfg_fp = open(os.path.join(*i))
        except IOError:
            continue
        else:
            break

    if not cfg_fp:
        raise FileNotFoundError("Config file not found!")

    config = ConfigParser()
    config.readfp(cfg_fp)

    return config


def parse_loglevel(name):
    """
    Parse log level name and return log level integer value
    """
    name = name.upper()

    if name in LOG_LEVELS:
        return getattr(logging, name, logging.INFO)

    return logging.INFO


def get_logging_config(config, name):
    """
    Prepare logging configuration for the sensor.

    Configuration set in config file, could be overwritten by sensor sections in config file.
    """
    level = config.get('global', 'loglevel', fallback=logging.INFO)
    filename = config.get('global', 'logfile', fallback='/tmp/sensor.log').strip()

    logconfig = {
        'format': config.get('global', 'logformat', fallback='%(asctime)s %(levelname)-8s %(name)s: %(message)s'),
        'filename': filename,
        'level': parse_loglevel(level),
    }

    if name in config:
        logconfig['filename'] = config.get(name,  'logfile', fallback=filename).strip()
        logconfig['level'] = parse_loglevel(config.get(name, 'loglevel', fallback=level))

    return logconfig


def zabbix_sender(config, trapper_item, value):
    if 'zabbix' in config:
        command = "zabbix_sender -z %s -s %s" % (config['zabbix']['server'], config['zabbix']['hostname'])

        if 'tls-connect' in config['zabbix']:
            command += " --tls-connect %s --tls-psk-identity \"%s\" --tls-psk-file %s " % \
                       (config['zabbix']['tls-connect'], config['zabbix']['tls-psk-identity'],
                        config['zabbix']['tls-psk-file'])

        command += " -k %s -o %s" % (trapper_item, value)

        process = subprocess.Popen([command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = process.communicate()


def mqtt_client(config):
    if 'mqtt' in config:
        client = mqtt.Client()

        if config['mqtt']['broker_url'] and config['mqtt']['broker_port']:
            client.username_pw_set(username="mqtt", password="mqtt")

        client.connect(config['mqtt']['broker_url'], config['mqtt']['broker_port'])
    else:
        client = None

    return client

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This software is licensed as described in the README.rst and LICENSE files,
# which you should have received as part of this distribution.
import os
import sys
import logging

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
        'format': config.get('global', 'logformat', fallback='%(asctime)s %(levelname)-8s %(name)s: %(message)s')
        'filename': filename,
        'level': parse_loglevel(level),
    }

    if name in config:
        logconfig['filename'] = config.get(name,  'logfile', fallback=filename).strip()
        logconfig['level'] = parse_loglevel(config.get(name, 'loglevel', fallback=level))

    return logconfig
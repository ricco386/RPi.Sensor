#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This software is licensed as described in the README.rst and LICENSE files,
# which you should have received as part of this distribution.
import sys
import logging

LOG_LEVELS = frozenset(['DEBUG', 'INFO', 'WARN', 'WARNING', 'ERROR', 'FATAL', 'CRITICAL'])


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
    logconfig = {
        'format': config.get('global', 'logformat', fallback='%(asctime)s %(levelname)-8s %(name)s: %(message)s'),
    }

    level = config.get('global', 'loglevel', fallback=logging.INFO)
    filename = config.get('global', 'logfile', fallback='')

    if name in config:
        level = config.get(name, 'loglevel', fallback=level)
        filename = config.get(name,  'logfile', fallback=filename)

    logconfig['level'] = parse_loglevel(level)

    if filename:
        logconfig['filename'] = filename.strip()
    else:
        logconfig['stream'] = sys.stdout

    return logconfig

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This software is licensed as described in the README.rst and LICENSE files,
# which you should have received as part of this distribution.
import logging

LOG_LEVELS = frozenset(['DEBUG', 'INFO', 'WARN', 'WARNING', 'ERROR', 'FATAL', 'CRITICAL'])


def get_journald_handler():
    try:
        from systemd.journal import JournaldLogHandler
    except ImportError:
        return None

    # instantiate the JournaldLogHandler to hook into systemd
    journald_handler = JournaldLogHandler()
    journald_handler.setFormatter(logging.Formatter(
        '[%(levelname)s] %(message)s'
    ))

    return journald_handler


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

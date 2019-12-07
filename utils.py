import os
import sys
import logging

from configparser import ConfigParser

LOG_LEVELS = frozenset(['DEBUG', 'INFO', 'WARN', 'WARNING', 'ERROR', 'FATAL', 'CRITICAL'])


def parse_loglevel(name):
    """Parse log level name and return log level integer value"""
    name = name.upper()

    if name in LOG_LEVELS:
        return getattr(logging, name, logging.INFO)

    return logging.INFO


def init_config_file():
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

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This software is licensed as described in the README.rst and LICENSE files,
# which you should have received as part of this distribution.
import os
import sys

from configparser import ConfigParser


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

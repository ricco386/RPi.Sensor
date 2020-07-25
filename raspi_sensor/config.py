#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This software is licensed as described in the README.rst and LICENSE files,
# which you should have received as part of this distribution.
import os
import sys

from configparser import ConfigParser


def init_config_file(cfg_location=None):
    """
    Load configuration file and search in different locations if it is not specified.
    """
    cfg_fp = None

    if cfg_location is None:
        cfg = 'sensor.cfg'
        # Try to read config file from ~/.sensor.cfg or /etc/sensor.cfg
        cfg_location = ((os.path.expanduser('~'), '.' + cfg), (sys.prefix, 'etc', cfg), ('/etc', cfg))

        for i in cfg_location:
            try:
                cfg_fp = open(os.path.join(*i))
            except IOError:
                continue
            else:
                break
    else:
        cfg_fp = open(cfg_location)

    if not cfg_fp:
        raise FileNotFoundError("Config file not found!")

    config = ConfigParser()
    config.read_file(cfg_fp)

    return config

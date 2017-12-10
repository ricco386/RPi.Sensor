#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This software is licensed as described in the README.rst and LICENSE files,
# which you should have received as part of this distribution.
import os
import sys
import RPi.GPIO as GPIO
from utils import parse_loglevel
import requests
import logging
import  time
try:
    # noinspection PyCompatibility
    from configparser import RawConfigParser
except ImportError:
    # noinspection PyCompatibility
    from ConfigParser import RawConfigParser


class Sensor(object):

    NAME = 'Sensor'
    LOGFORMAT = '%(asctime)s %(levelname)-8s %(name)s: %(message)s'

    sensor_pin = None
    thread_exit = False
    cycle_sleep = False
    failed = 0

    def __init__(self, args=[]):
        self.logger = logging.getLogger(self.NAME)

        cfg = 'sensor.cfg'
        cfg_fp = None
        cfg_lo = ((os.path.expanduser('~'), '.' + cfg), (sys.prefix, 'etc', cfg), ('/etc', cfg))
        config_base_sections = ('global',)

        # Try to read config file from ~/.sensor.cfg or /etc/sensor.cfg
        for i in cfg_lo:
            try:
                cfg_fp = open(os.path.join(*i))
            except IOError:
                continue
            else:
                break

        if not cfg_fp:
            sys.stderr.write("""\nSensor can't start!\n
You need to create a config file in one these locations: \n%s\n
You can rename sensor.cfg.example and update the required options.
The example file is located in: %s\n\n""" % (
    '\n'.join([os.path.join(*i) for i in cfg_lo]),
    os.path.dirname(os.path.abspath(__file__))))
            sys.exit(1)

        # Read and parse configuration
        # noinspection PyShadowingNames
        def load_config(fp, reopen=False):
            config = RawConfigParser()
            if reopen:
                fp = open(fp.name)
            config.readfp(fp)  # TODO: Deprecated since python 3.2
            fp.close()
            return config
        self.config = load_config(cfg_fp)

        # Prepare logging configuration
        logconfig = {
            'level': parse_loglevel(self.config.get('global', 'loglevel')),
            'format': self.LOGFORMAT,
        }

        if self.config.has_option('global', 'logfile'):
            logfile = self.config.get('global', 'logfile').strip()
            if logfile:
                logconfig['filename'] = logfile

        # Setup logging
        logging.basicConfig(**logconfig)
        self.logger.info('Loaded configuration from %s', cfg_fp.name)

    def sensor_setup(self):
        self.logger.debug('Initial sensor setup.')

        self.sensor_pin =  self.config.get(self.NAME, 'sensor_pin')
        self.logger.info('Sensor at PIN: %s' % self.sensor_pin)
        self.set_gpio()

    def sensor_cleanup(self):
        self.GPIO.cleanup()

    def set_gpio(self):
        self.GPIO = GPIO
        self.GPIO.setmode(GPIO.BOARD)
        self.GPIO.setup(self.sensor_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def failed_notification(self):
        if self.config.has_option('global', 'failed_notify') and \
                self.failed >= self.config.get('global', 'failed_notify'):
            self.logger.warning('Sensor reading has failed %s in a row.' % self.failed)

    def pre_sensor_read_callback(self):
        self.logger.debug('Pre-read sensor callback.')

    def sensor_read_callback(self):
        self.logger.debug('Sensor read callback.')

    def post_sensor_read_callback(self):
        self.logger.debug('Post-read sensor callback.')
        self.failed_notification()

    def sensor_read(self):
        self.pre_sensor_read_callback()
        self.sensor_read_callback()
        self.post_sensor_read_callback()

    def sense(self):
        try:
            self.logger.debug('Starting permanent sensing process...')
            self.sensor_setup()

            while not self.thread_exit:
                self.sensor_read()

                if self.cycle_sleep:
                    time.sleep(self.cycle_sleep)

                if self.thread_exit:
                    self.logger.info('Signal send to interupted sensing process...')

        except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
            self.logger.info('You have interupted sensing process...')

        self.sensor_cleanup()

    def post_data(self, path, postdata):
        if not self.config.has_option('server', 'hostname'):
            self.logger.error('Trying to post data, but no server bas been defined!')
            raise ValueError('Server has not been defined!')
        else:
            url = '%s/%s' % (self.config.get('server', 'hostname'), path)

        r = requests.get(url)
        if not self.verify_server_response(r):
            return False

        if self.config.has_option('server', 'token'):
            headers = {
                'Authorization': 'Token %s' % (self.config.get('server', 'token'),)
            }
            r = requests.post(url, headers=headers, data=postdata)
        elif self.config.has_option('server', 'username') and self.config.has_option('server', 'password'):
            r = requests.post(url, auth=(self.config.get('server', 'username'), self.config.get('server', 'password')), data=postdata)
        else:
            r = requests.post(url, data=postdata)

        return self.verify_server_response(r)

    def verify_server_response(self, r):
        if r.status_code in (200, 201, 202, 203, 204, 205, 206):
            self.logger.info("SUCCESSFUL HTTP %s response %s: %s." % (r.request.method, r.status_code, r.reason))
            return True

        else:
            self.logger.error("FAILED HTTP %s response %s: %s." % (r.request.method, r.status_code, r.reason))
            return False

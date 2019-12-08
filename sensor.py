#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This software is licensed as described in the README.rst and LICENSE files,
# which you should have received as part of this distribution.
import logging
import time
import signal

import RPi.GPIO as GPIO

from utils import parse_loglevel, init_config_file


class Sensor(object):

    NAME = 'Sensor'
    PIN = None
    GPIO = None
    GPIO_BCM = False
    FAILED = 0
    FAILED_NOTIF = 10
    SLEEP = 0
    EXIT = False

    def __init__(self):
        self.logger = logging.getLogger(self.NAME)
        self.config = init_config_file()
        # Prepare logging configuration
        logconfig = {
            'filename': self.config.get('global', 'logfile', fallback='/tmp/sensor.log').strip(),
            'level': parse_loglevel(self.config.get('global', 'loglevel', fallback=logging.INFO)),
            'format': self.config.get('global', 'logformat', fallback='%(asctime)s %(levelname)-8s %(name)s: %(message)s')
        }
        # Setup logging
        logging.basicConfig(**logconfig)

        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

        self.sensor_setup()

    def exit_gracefully(self, signum, frame):
        self.EXIT = True
        self.logger.info('Sensor %s received interrupt signal.', self.NAME)

    def sensor_setup(self):
        """
        Initial function to configure sensor before the main infinite loop
        """
        self.logger.debug('Sensor %s initial setup.', self.NAME)
        cycle_sleep = False
        sensor_failed_notif = False

        if self.NAME in self.config:
            self.PIN = int(self.config.get(self.NAME, 'sensor_pin', fallback=self.PIN))
            self.GPIO_BCM = bool(self.config.get(self.NAME, 'gpio_bcm', fallback=self.GPIO_BCM))
            cycle_sleep = int(self.config.get(self.NAME, 'cycle_sleep', fallback=0))
            sensor_failed_notif = int(self.config.get(self.NAME, 'failed_notify', fallback=0))

        if cycle_sleep:
            self.SLEEP = cycle_sleep
        else:
            self.SLEEP = int(self.config.get('global', 'cycle_sleep', fallback=0))

        if sensor_failed_notif:
            self.FAILED_NOTIF = sensor_failed_notif
        else:
            self.FAILED_NOTIF = int(self.config.get('global', 'failed_notify', fallback=10))

        self.logger.debug('Sensor %s at cycle_sleep: %s.', self.NAME, self.SLEEP)
        self.logger.debug('Sensor %s at failed_notify: %s.', self.NAME, self.FAILED_NOTIF)

    def gpio_setup(self, gpio_bcm=False):
        self.GPIO = GPIO

        if gpio_bcm:
            self.GPIO.setmode(GPIO.BCM)
            self.logger.debug('Sensor %s mode set to GPIO.BCM.', self.NAME)
        else:
            self.GPIO.setmode(GPIO.BOARD)
            self.logger.debug('Sensor %s mode set to GPIO.BOARD', self.NAME)

        self.GPIO.setup(self.PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.logger.info('Sensor %s at PIN: %s.', self.NAME, self.PIN)

    def gpio_cleanup(self):
        self.GPIO.cleanup()
        self.logger.debug('Sensor %s GPIO cleanup.', self.NAME)

    def failed_notification_callback(self):
        pass

    def pre_sensor_read_callback(self):
        """
        Helper function with code to be run before reading the sensor
        """
        # self.logger.debug('Pre-read sensor callback.')  # Do not spam the log
        if self.GPIO is None:
            self.gpio_setup(self.GPIO_BCM)

    def sensor_read_callback(self):
        """
        Implement logic for actual sensor reading
        """
        raise NotImplementedError()

    def post_sensor_read_callback(self):
        """
        Helper function with code to be run after reading the sensor
        """
        # self.logger.debug('Post-read sensor callback.')  # Do not spam the log
        if self.FAILED >= self.FAILED_NOTIF:
            self.logger.warning('Sensor reading has failed %s in a row.' % self.FAILED)
            self.failed_notification_callback()

    def sensor_read(self):
        self.pre_sensor_read_callback()
        self.sensor_read_callback()
        self.post_sensor_read_callback()

    def sense(self):
        """
        Main sensor function to run!
        """
        self.logger.debug('Sensor %s starting permanent sensing process...', self.NAME)

        while not self.EXIT:
            self.sensor_read()

            if self.SLEEP:
                time.sleep(self.SLEEP)

        self.gpio_cleanup()
        self.logger.info('Sensor %s has correctly finished sensing... BYE!', self.NAME)

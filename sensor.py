#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This software is licensed as described in the README.rst and LICENSE files,
# which you should have received as part of this distribution.
import logging
import time
import signal

import RPi.GPIO as GPIO

from utils import init_config_file, get_logging_config


class Sensor(object):

    NAME = 'Sensor'
    PIN = None
    GPIO = None
    GPIO_BCM = False
    FAILED = 0
    FAILED_NOTIF = 10
    SLEEP = 0.05
    EXIT = False
    sensor_state = 0

    def __init__(self, name='Sensor', params=()):
        self.NAME = name
        self.config = init_config_file()

        # Setup logging
        self.logger = logging.getLogger(self.NAME)
        logging.basicConfig(**get_logging_config(self.config, self.NAME))

        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

        self.setup_sensor()
        self.setup_args(params)  # Should overwrite the default options in config file

    def exit_gracefully(self, signum, frame):
        self.EXIT = True
        self.logger.info('Sensor %s received interrupt signal.', self.NAME)

    def setup_sensor(self):
        """
        Initial function to configure sensor before the main infinite loop
        """
        self.logger.debug('Sensor %s initial setup.', self.NAME)
        self.SLEEP = float(self.config.get('global', 'cycle_sleep', fallback=0.05))
        self.FAILED_NOTIF = int(self.config.get('global', 'failed_notify', fallback=10))

        if self.NAME in self.config:
            self.PIN = int(self.config.get(self.NAME, 'sensor_pin', fallback=self.PIN))
            self.GPIO_BCM = bool(self.config.get(self.NAME, 'gpio_bcm', fallback=self.GPIO_BCM))
            self.SLEEP = float(self.config.get(self.NAME, 'cycle_sleep', fallback=self.SLEEP))
            self.FAILED_NOTIF = int(self.config.get(self.NAME, 'failed_notify', fallback=self.FAILED_NOTIF))

        self.logger.debug('Sensor %s at cycle_sleep: %s.', self.NAME, self.SLEEP)
        self.logger.debug('Sensor %s at failed_notify: %s.', self.NAME, self.FAILED_NOTIF)

    def setup_args(self, params):
        if hasattr(params, 'pin') and params.pin:
            self.PIN = params.pin
            self.logger.info('Sensor %s at PIN: %s (set by script parameter).', self.NAME, self.PIN)

        if hasattr(params, 'gpio_bcm') and params.gpio_bcm:
            self.GPIO_BCM = True
            self.logger.info('Sensor %s mode set to GPIO.BCM (set by script parameter).', self.NAME)

        if hasattr(params, 'cycle_sleep') and params.cycle_sleep:
            self.SLEEP = params.cycle_sleep
            self.logger.debug('Sensor %s at cycle_sleep: %s (set by script parameter).', self.NAME, self.SLEEP)

        if hasattr(params, 'failed_notify') and params.failed_notify:
            self.FAILED_NOTIF = params.failed_notify
            self.logger.debug('Sensor %s at failed_notify: %s (set by script parameter).', self.NAME, self.FAILED_NOTIF)

    def gpio_setup(self):
        self.GPIO = GPIO

        if self.GPIO_BCM:
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
        if self.GPIO is None:
            self.gpio_setup()

    def sensor_read_callback(self):
        """
        Implement logic for actual sensor reading
        """
        raise NotImplementedError()

    def post_sensor_read_callback(self):
        """
        Helper function with code to be run after reading the sensor
        """
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

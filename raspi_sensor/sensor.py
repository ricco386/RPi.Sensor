#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This software is licensed as described in the README.rst and LICENSE files,
# which you should have received as part of this distribution.
import logging
import time
import signal
import sys

import RPi.GPIO as GPIO
from math import inf

from .config import init_config_file
from .logging import get_logging_config


class Sensor(object):

    NAME = 'Sensor'
    PIN = None
    GPIO = None
    GPIO_BCM = False
    GPIO_OUT = False
    FAILED = 0
    FAILED_NOTIF = 10
    FAILED_EXIT = inf
    SLEEP = 0.05
    EXIT = False
    sensor_state = 0

    def __init__(self, name='Sensor', config_path=None):
        self.NAME = name
        self.config = init_config_file(cfg_location=config_path)

        # Setup logging
        self.logger = logging.getLogger(self.NAME)
        logging.basicConfig(**get_logging_config(self.config, self.NAME))

        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

        self.setup_sensor()

    def exit_gracefully(self, signum, frame):
        self.EXIT = True
        self.logger.info('Sensor %s received interrupt signal', self.NAME)

    def exit_callback(self):
        self.gpio_cleanup()

    def setup_sensor(self):
        """
        Initial function to configure sensor before the main infinite loop
        """
        self.logger.debug('Sensor %s initial setup', self.NAME)
        self.SLEEP = float(self.config.get('global', 'cycle_sleep', fallback=self.SLEEP))
        self.FAILED_NOTIF = int(self.config.get('global', 'failed_notify', fallback=self.FAILED_NOTIF))
        self.FAILED_EXIT = float(self.config.get('global', 'failed_exit', fallback=self.FAILED_EXIT))

        if self.NAME in self.config:
            self.PIN = int(self.config.get(self.NAME, 'sensor_pin', fallback=self.PIN))
            self.GPIO_BCM = bool(self.config.get(self.NAME, 'gpio_bcm', fallback=self.GPIO_BCM))
            self.GPIO_OUT = bool(self.config.get(self.NAME, 'gpio_out', fallback=self.GPIO_OUT))
            self.SLEEP = float(self.config.get(self.NAME, 'cycle_sleep', fallback=self.SLEEP))
            self.FAILED_NOTIF = int(self.config.get(self.NAME, 'failed_notify', fallback=self.FAILED_NOTIF))
            self.FAILED_EXIT = float(self.config.get(self.NAME, 'failed_exit', fallback=self.FAILED_EXIT))

        self.logger.debug('Sensor %s at cycle_sleep: %s', self.NAME, self.SLEEP)
        self.logger.debug('Sensor %s at failed_notify: %s', self.NAME, self.FAILED_NOTIF)
        self.logger.debug('Sensor %s at failed_exit: %s', self.NAME, self.FAILED_EXIT)

    def setup_args(self, params):
        if hasattr(params, 'pin') and params.pin:
            self.PIN = params.pin
            self.logger.info('Sensor %s at PIN: %s (set by script parameter)', self.NAME, self.PIN)

        if hasattr(params, 'gpio_bcm') and params.gpio_bcm:
            self.GPIO_BCM = True
            self.logger.info('Sensor %s mode set to GPIO.BCM (set by script parameter)', self.NAME)

        if hasattr(params, 'gpio_out') and params.gpio_out:
            self.GPIO_OUT = True
            self.logger.info('Sensor %s mode set to GPIO.OUT (set by script parameter)', self.NAME)

        if hasattr(params, 'cycle_sleep') and params.cycle_sleep:
            self.SLEEP = params.cycle_sleep
            self.logger.debug('Sensor %s at cycle_sleep: %s (set by script parameter)', self.NAME, self.SLEEP)

        if hasattr(params, 'failed_notify') and params.failed_notify:
            self.FAILED_NOTIF = params.failed_notify
            self.logger.debug('Sensor %s at failed_notify: %s (set by script parameter)', self.NAME, self.FAILED_NOTIF)

        if hasattr(params, 'failed_exit') and params.failed_exit:
            self.FAILED_EXIT = params.failed_exit
            self.logger.debug('Sensor %s at failed_exit: %s (set by script parameter)', self.NAME, self.FAILED_EXIT)

    def gpio_setup(self):
        self.GPIO = GPIO

        if self.GPIO_BCM:
            self.GPIO.setmode(GPIO.BCM)
            self.logger.debug('Sensor %s mode set to GPIO.BCM', self.NAME)
        else:
            self.GPIO.setmode(GPIO.BOARD)
            self.logger.debug('Sensor %s mode set to GPIO.BOARD', self.NAME)

        if self.GPIO_OUT:
            self.GPIO.setup(self.PIN, GPIO.OUT)
        else:
            self.GPIO.setup(self.PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        self.logger.info('Sensor %s at PIN: %s', self.NAME, self.PIN)

    def gpio_cleanup(self):
        self.GPIO.cleanup()
        self.logger.debug('Sensor %s GPIO cleanup', self.NAME)

    def failed_notification_callback(self):
        self.logger.warning('Sensor reading has failed %s in a row.' % self.FAILED)

    def pre_sensor_read_callback(self):
        """
        Helper function with code to be run before reading the sensor
        """
        if self.GPIO is None:
            self.gpio_setup()

    @staticmethod
    def calculate_change_percentage(value, previous_value):
        if previous_value is None or value is None:
            percentage = 0
        else:
            difference = previous_value - value
            percentage = difference / value * 100

        return percentage

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
            self.failed_notification_callback()

        if self.FAILED >= self.FAILED_EXIT:
            self.logger.error('Sensor reading has failed to many times... Exit!')
            self.exit_callback()
            sys.exit(1)

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

        self.exit_callback()
        self.logger.info('Sensor %s has correctly finished sensing... BYE!', self.NAME)

    def notify(self, topic=None, payload=None):
        pass

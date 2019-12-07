#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This software is licensed as described in the README.rst and LICENSE files,
# which you should have received as part of this distribution.
import logging
import time
import signal

import RPi.GPIO as GPIO

from .utils import parse_loglevel, init_config_file


class Sensor(object):

    NAME = 'Sensor'
    PIN = None
    SLEEP = False
    EXIT = False
    FAILED = 0
    FAILED_NOTIF = 10

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

    def exit_gracefully(self, signum, frame):
        self.EXIT = True
        self.logger.info('Sensor %s received interrupt signal.', self.NAME)

    def sensor_setup(self):
        """
        Initial function to configure sensor before the main infinite loop
        """
        self.logger.debug('Sensor %s initial setup.', self.NAME)

        self.PIN = self.config.get(self.NAME, 'sensor_pin')
        self.logger.info('Sensor %s at PIN: %s.', self.NAME, self.PIN)

        self.SLEEP = self.config.get(self.NAME, 'cycle_sleep', fallback=False)
        self.logger.info('Sensor %s at cycle sleep: %s.', self.NAME, self.SLEEP)

        sensor_failed_notif = self.config.get(self.NAME, 'failed_notify', fallback=False)

        if not sensor_failed_notif:
            self.FAILED_NOTIF = self.config.get('global', 'failed_notify', fallback=10)
        else:
            self.FAILED_NOTIF = sensor_failed_notif

        self.config.get('global', 'failed_notify', fallback=10)

        self.gpio_setup()

    def gpio_cleanup(self):
        self.GPIO.cleanup()
        self.logger.debug('Sensor %s GPIO cleanup.', self.NAME)

    def gpio_setup(self):
        self.GPIO = GPIO
        self.GPIO.setmode(GPIO.BOARD)
        self.GPIO.setup(self.PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.logger.debug('Sensor %s GPIO set.', self.NAME)

    def failed_notification_callback(self):
        pass

    def pre_sensor_read_callback(self):
        """
        Helper function with code to be run before reading the sensor
        """
        self.logger.debug('Pre-read sensor callback.')

    def sensor_read_callback(self):
        """
        Implement logic for actual sensor reading
        """
        raise NotImplementedError()

    def post_sensor_read_callback(self):
        """
        Helper function with code to be run after reading the sensor
        """
        self.logger.debug('Post-read sensor callback.')

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
        if self.NAME == 'Sensor':
            raise NotImplementedError('Sensor NAME has to be defined!')

        self.logger.debug('Sensor %s starting permanent sensing process...', self.NAME)
        self.sensor_setup()

        while not self.thread_exit:
            try:
                self.sensor_read()

                if self.SLEEP:
                    time.sleep(self.SLEEP)

            except KeyboardInterrupt:  # If CTRL+C is pressed, exit cleanly:
                self.EXIT = True
                self.logger.info('Sensor %s you have interrupted sensing process...', self.NAME)

        self.gpio_cleanup()

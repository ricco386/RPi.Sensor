#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This software is licensed as described in the README.rst and LICENSE files,
# which you should have received as part of this distribution.
import argparse
from sensor import Sensor


def setup_args():
    ap = argparse.ArgumentParser(prog='rpi-sensor', description='''Python base class to create infinite loop to work 
    with sensors. Script loads configuration from sensor.cfg that has to be created and run in infinte loop. For more
    info visit: https://github.com/ricco386/RPi.Sensor''')
    ap.add_argument('-p', '--pin', type=int, help='GPIO pin number..')
    ap.add_argument('--gpio_bcm', action='store_true', help='Switch PIN numbers to GPIO BCM numbering.')
    ap.add_argument('--failed_notify', type=int, help='Number of failed sensor reading before alerting.')
    ap.add_argument('--cycle_sleep', type=int, help='Number of failed sensor reading before alerting.')

    return ap.parse_args()


def main():
    s = Sensor()
    args = setup_args()

    if hasattr(args, 'gpio_bcm') and args.gpio_bcm:
        s.GPIO_BCM = True
        s.logger.debug('Sensor %s mode set to GPIO.BCM (set by script parameter).', s.NAME)

    if hasattr(args, 'pin') and args.pin:
        s.PIN = args.pin
        s.logger.info('Sensor %s at PIN: %s (set by script parameter).', s.NAME, s.PIN)

    if hasattr(args, 'failed_notify') and args.failed_notify:
        s.FAILED_NOTIF = args.failed_notify
        s.logger.debug('Sensor %s at failed_notify: %s (set by script parameter).', s.NAME, s.FAILED_NOTIF)

    if hasattr(args, 'cycle_sleep') and args.cycle_sleep:
        s.SLEEP = args.cycle_sleep
        s.logger.debug('Sensor %s at cycle_sleep: %s (set by script parameter).', s.NAME, s.SLEEP)

    s.sensor_read()  # If you want to read just  once
    s.sense()  # Start infinite loop (You can finish by CTRL+C or send kill signal)


if __name__ == "__main__":
    # execute only if run as a script
    main()
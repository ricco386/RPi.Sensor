#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This software is licensed as described in the README.rst and LICENSE files,
# which you should have received as part of this distribution.
import argparse
from .sensor import Sensor


def setup_default_args(ap):
    ap.add_argument('-n', '--name', type=str, help='Sensor name.')
    ap.add_argument('-p', '--pin', type=int, help='GPIO pin number.')
    ap.add_argument('-s', '--status', action='store_true', help='Get current sensor reading.')
    ap.add_argument('--gpio_bcm', action='store_true', help='Switch PIN numbers to GPIO BCM numbering.')
    ap.add_argument('--gpio_out', action='store_true', help='Switch PIN to be in output mode it can be configured to '
                                                            'high or low.')
    ap.add_argument('--failed_notify', type=int, help='Number of failed sensor reading before alerting.')
    ap.add_argument('--failed_exit', type=int, help='Number of failed sensor reading before exiting.')
    ap.add_argument('--cycle_sleep', type=int, help='Number of failed sensor reading before alerting.')
    ap.add_argument('-c', '--config', type=str, help='Path to the sensor configuration file.')

    return ap


def setup_default_mqtt_args(ap):
    setup_default_args(ap)
    ap.add_argument('--mqtt_topic', type=str, help='Set topic for MQTT where sensor will publish data.')

    return ap


def setup_args():
    ap = argparse.ArgumentParser(prog='raspi-sensor',
                                 description='Python base class to create infinite loop to work with sensors. For more '
                                             'info visit: https://github.com/ricco386/RPi.Sensor')
    setup_default_args(ap)

    return ap.parse_args()


def main():
    name = 'Sensor'
    params = setup_args()

    if hasattr(params, 'name') and params.name:
        name = params.name

    s = Sensor(name=name)
    s.setup_args(params)

    if hasattr(params, 'status') and params.status:
        s.sensor_read()  # If you want to read just once
    else:
        s.sense()  # Start infinite loop (You can finish by CTRL+C or send kill signal)


if __name__ == "__main__":
    # execute only if run as a script
    main()

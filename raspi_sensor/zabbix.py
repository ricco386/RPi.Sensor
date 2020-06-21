#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This software is licensed as described in the README.rst and LICENSE files,
# which you should have received as part of this distribution.
import subprocess


def zabbix_sender(config, trapper_item, value):
    if 'zabbix' in config:
        command = "zabbix_sender -z %s -s %s" % (config['zabbix']['server'], config['zabbix']['hostname'])

        if 'tls-connect' in config['zabbix']:
            command += " --tls-connect %s --tls-psk-identity \"%s\" --tls-psk-file %s " % \
                       (config['zabbix']['tls-connect'], config['zabbix']['tls-psk-identity'],
                        config['zabbix']['tls-psk-file'])

        command += " -k %s -o %s" % (trapper_item, value)

        process = subprocess.Popen([command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = process.communicate()

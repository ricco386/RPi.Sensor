import logging
from raspi_sensor.logging import parse_loglevel


def test_parse_loglevel():
    assert parse_loglevel('UNKNOWN') == logging.INFO
    assert parse_loglevel('DEBUG') == logging.DEBUG
    assert parse_loglevel('INFO') == logging.INFO
    assert parse_loglevel('WARN') == logging.WARN
    assert parse_loglevel('WARNING') == logging.WARNING
    assert parse_loglevel('ERROR') == logging.ERROR
    assert parse_loglevel('FATAL') == logging.FATAL
    assert parse_loglevel('CRITICAL') == logging.CRITICAL

    assert parse_loglevel('unknown') == logging.INFO
    assert parse_loglevel('debug') == logging.DEBUG
    assert parse_loglevel('info') == logging.INFO
    assert parse_loglevel('warn') == logging.WARN
    assert parse_loglevel('warning') == logging.WARNING
    assert parse_loglevel('error') == logging.ERROR
    assert parse_loglevel('fatal') == logging.FATAL
    assert parse_loglevel('critical') == logging.CRITICAL

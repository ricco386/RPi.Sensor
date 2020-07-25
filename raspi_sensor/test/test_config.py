import pytest

from configparser import ConfigParser
from raspi_sensor.config import init_config_file
from raspi_sensor.sensor import Sensor


def test_init_config_file():
    with pytest.raises(FileNotFoundError):
        init_config_file()

    config = init_config_file(cfg_location='raspi_sensor/sensor.cfg.example')
    assert isinstance(config, ConfigParser)


def test_sensor_instance_config_values():
    # Sensor EXAMPLE is in sample config, load values from config
    s = Sensor(name='Sensor EXAMPLE', config_path='raspi_sensor/sensor.cfg.example')
    assert s.NAME == 'Sensor EXAMPLE'
    assert s.PIN == 11
    assert s.GPIO_BCM is True
    assert s.GPIO_OUT is True
    assert s.FAILED_NOTIF == 5
    assert s.FAILED_EXIT == 50
    assert s.SLEEP == 60

    # Sensor TEST is NOT in sample config, load defaults in object
    s = Sensor(name='Sensor TEST', config_path='raspi_sensor/sensor.cfg.example')
    assert s.NAME == 'Sensor TEST'
    assert s.PIN is None
    assert s.GPIO_BCM is False
    assert s.GPIO_OUT is False
    assert s.FAILED_NOTIF == 7
    assert s.FAILED_EXIT == 15
    assert s.SLEEP == 0.1

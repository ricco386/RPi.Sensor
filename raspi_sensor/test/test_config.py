import pytest

from configparser import ConfigParser
from raspi_sensor.config import init_config_file
from raspi_sensor.sensor import Sensor
from raspi_sensor.mqtt import MqttSensor


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


def test_mqtt_sensor_instance_config_values():
    # Sensor EXAMPLE is in sample config, load values from config
    s = MqttSensor(name='Sensor EXAMPLE', config_path='raspi_sensor/sensor.cfg.example', autoconnect=False)
    assert s.NAME == 'Sensor EXAMPLE'
    assert s.PIN == 11
    assert s.GPIO_BCM is True
    assert s.GPIO_OUT is True
    assert s.FAILED_NOTIF == 5
    assert s.FAILED_EXIT == 50
    assert s.SLEEP == 60
    assert s.topic == "example/test"
    assert s.broker_url == 'mqtt.example.com'
    assert s.broker_port == 1884
    assert s.broker_keepalive == 950
    assert s.availability_notif_period == 900

    # Sensor TEST is NOT in sample config, load defaults in object
    s = MqttSensor(name='Sensor TEST', config_path='raspi_sensor/sensor.cfg.example', autoconnect=False)
    assert s.NAME == 'Sensor TEST'
    assert s.PIN is None
    assert s.GPIO_BCM is False
    assert s.GPIO_OUT is False
    assert s.FAILED_NOTIF == 7
    assert s.FAILED_EXIT == 15
    assert s.SLEEP == 0.1
    assert s.topic == ''
    assert s.broker_url == 'mqtt.example.com'
    assert s.broker_port == 1884
    assert s.broker_keepalive == 950
    assert s.availability_notif_period == 900

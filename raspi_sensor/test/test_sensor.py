import pytest

from raspi_sensor.sensor import Sensor


def test_calculate_change_percentage():
    assert Sensor.calculate_change_percentage(None, None) == 0
    assert Sensor.calculate_change_percentage(23, 23) == 0
    assert Sensor.calculate_change_percentage(10, 100) == 900
    assert Sensor.calculate_change_percentage(100, 10) == -90
    assert Sensor.calculate_change_percentage(50, 100) == 100
    assert Sensor.calculate_change_percentage(100, 50) == -50
    assert Sensor.calculate_change_percentage(23.8, 21.5) == -9.66386554621849


def test_sensor_instance_config_values():
    # Sensor EXAMPLE is in sample config, load values from config
    s = Sensor(name='Sensor EXAMPLE', config_path='raspi_sensor/sensor.cfg.example')

    with pytest.raises(NotImplementedError):
        s.sense()

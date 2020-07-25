import pytest

from raspi_sensor.mqtt import MqttSensor


def test_sensor_instance_config_values():
    # Sensor EXAMPLE is in sample config, load values from config
    s = MqttSensor(name='Sensor EXAMPLE', config_path='raspi_sensor/sensor.cfg.example', autoconnect=False)

    with pytest.raises(NotImplementedError):
        s.sense()

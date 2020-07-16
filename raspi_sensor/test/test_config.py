import pytest

from configparser import ConfigParser
from raspi_sensor.config import init_config_file


def test_init_config_file():
    with pytest.raises(FileNotFoundError):
        init_config_file()

    config = init_config_file((('raspi_sensor', 'sensor.cfg.example'),))
    assert isinstance(config, ConfigParser)

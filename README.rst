RPi.Sensor
##########

.. image:: https://github.com/ricco386/RPi.Sensor/workflows/Test%20RPi.Sensor%20codebase/badge.svg
.. image:: https://github.com/ricco386/RPi.Sensor/workflows/Release%20RPi.Sensor%20to%20PyPI/badge.svg

Generic Python base class to create infinite loop to work with different sensors connected to Raspberry Pi. Project
contains also extended Python base class with MQTT support.

RPi.Sensor library is stable in terms of running as a base class. Sensor logic and additional functionality before and
after sensor measurement should be implemented in child objects anyway... But there are new features developed (and
bug fixed as they are found) so it is recommended always use the latest version.

If you want to see example of implemented sensors, have a look at my other `RPi repo <https://github.com/ricco386/RPi>`_.

Installation
------------

- Install the latest released version using pip::

    pip install https://github.com/ricco386/RPi.Sensor/zipball/master

- Alternatively install latest released version from pypi::

    pip install --upgrade RPi.Sensor

- Make sure all dependencies (listed below) are installed (done automatically when installing via pip)

**Dependencies:**

- `RPi.GPIO <https://pypi.python.org/pypi/RPi.GPIO/>`_
- `wheel <https://pypi.org/project/wheel/>`_
- `paho-mqtt <https://pypi.org/project/paho-mqtt/>`_

Usage
-----

Inherit Sensor object or MqttSensor.

Main purpose of the sensor object is to run infinite loop for reading from the sensors. Object has build in basic
functionality to terminate the infinite loop correctly (uppon CTRL+C or kill signal), basic logging etc.

Intention is to have ability to easily run some code before (or after) reading the sensor, this is is skeleton that
doesnt do any logic and should be used only as a base for building the interactions with the sensors.

If you want to see example of implemented sensors, have a look at my other `RPi repo <https://github.com/ricco386/RPi>`_.

If you find a security vulnerability please read through
`SECURITY.rst <https://github.com/ricco386/RPi.Sensor/blob/master/SECURITY.rst>`_ file and report it responsibly. All
other issues and feature requests report via `Github issue tracker <https://github.com/ricco386/RPi.Sensor/issues>`_.

License
-------

For more information see the `LICENSE <https://github.com/ricco386/RPi.Sensor/blob/master/LICENSE>`_ file.

RPi.Sensor
##########

Generic Python base class to create infinite loop to work with different sensors connected to Raspberry Pi.

Installation
------------

- Install the latest released version using pip::

    pip install https://github.com/ricco386/RPi.Sensor/zipball/master

- Make sure all dependencies (listed below) are installed (done automatically when installing via pip)

**Dependencies:**

- `RPi.GPIO <https://pypi.python.org/pypi/RPi.GPIO>`_
- `wheel <https://pypi.org/project/wheel/>`_

Usage
-----

Inherit Sensor object.

Main purpose of the sensor object is to run infinite loop for reading from the sensors. Object has build in basic functionality to terminate the infinite loop correctly, basic logging etc.

Intention is to have ability to easily run some code before (or after) reading the sensor, this is is skelleton that doesnt do any logic and should be used only as a base for building the interactions with the sensors.

License
-------

For more information see the `LICENSE <https://github.com/ricco386/RPi.Sensor/blob/master/LICENSE>`_ file.

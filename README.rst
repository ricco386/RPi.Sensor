RPi.Sensor
##########

Generic Class for Pythonsensor objects connected to Raspberry Pi.

Installation
------------

- Install the latest released version using pip::

    pip install https://github.com/ricco386/RPi.Sensor/zipball/master

- Make sure all dependencies (listed below) are installed (done automatically when installing via pip)

**Dependencies:**

- `RPi.GPIO <https://pypi.python.org/pypi/RPi.GPIO>`_ (0.6.1+)

Usage
-----

Inherit Sensor object.
Sensor object already does some basic logging, and simple argparse for cmdline scripts. It also does create infinite loop for running sensor and has flag to finish the loop it is is called in a thread.

License
-------

For more information see the `LICENSE <https://github.com/ricco386/RPi.Sensor/blob/master/LICENSE>`_ file.

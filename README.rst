=========================================
Publish RuuviTag sensor data with LoRaWAN
=========================================

This repository contains the up to date snippets for the "Publish RuuviTag sensor data on The Things Network" tutorial. (**WIP**)

This example code uses settings specifically for connecting to The Things Network within the European 868 MHz region. For another usage, please see the settings.py and node.py file for relevant sections that need changing.


Requirements
------------

* `MicroPython RuuviTag Scanner <https://github.com/rroemhild/micropython-ruuvitag>`_


Data Format
-----------

For each RuuviTag scanned we send 5 bytes.

+--------+---------------------------------------------+
| Offset | Description                                 |
+========+=============================================+
| 0      | Tag ID (8bit)                               |
+--------+---------------------------------------------+
| 1-2    | Temperature in 0.005 degrees (16bit signed) |
+--------+---------------------------------------------+
| 3-4    | Humidity in 0.0025% (16bit unsigned)        |
+--------+---------------------------------------------+

In example for 2 RuuviTags the follwoing payload will be send:

.. code-block:: python

    b'\x00\x11\x8aZ\xd0\x01\x06&y\xe0'

+----+------+------+----+------+------+
| ID | Temp | Hum  | ID | Temp | Hum  |
+====+======+======+====+======+======+
| 00 | 118A | 5AD0 | 01 | 0626 | 79E0 |
+----+------+------+----+------+------+

You can read more about the data format used in this project in the `Ruuvi Sensor Data Format 5 Protocol Specification <https://github.com/ruuvi/ruuvi-sensor-protocols#data-format-5-protocol-specification>`_.


Payload Format Decoder
----------------------

Example payload format decoder for the The Things Network Console:

.. code-block:: javascript

    function Decoder(bytes, port) {
      var ruuvitags = {};
      var tagname = "";
      var tags = bytes.length / 5;

      for (i=0;i<tags;i+=1) {
        var temperature = (bytes[1] << 8) | bytes[2];
        var humidity = (bytes[3] << 8) | bytes[4];

        if (bytes[0] === 0) {
          tagname = "livingroom";
        }
        else if (bytes[0] === 1) {
          tagname = "bathroom";
        }

        ruuvitags[tagname] = {
            "humidity": parseFloat((humidity * 0.0025).toFixed(2)),
            "temperature": parseFloat((temperature * 0.005).toFixed(2))
        };

        bytes.splice(0, 5);
      }

      ruuvitags.num = tags;
      return ruuvitags;
    }

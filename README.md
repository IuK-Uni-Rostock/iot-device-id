IoT Device ID
=============

[![Build Status](https://travis-ci.org/IuK-Uni-Rostock/iot-device-id.svg?branch=master)](https://travis-ci.org/IuK-Uni-Rostock/iot-device-id)
[![Coverage Status](https://coveralls.io/repos/github/IuK-Uni-Rostock/iot-device-id/badge.svg?branch=master)](https://coveralls.io/github/IuK-Uni-Rostock/iot-device-id?branch=master)

IoT Device ID can detect IoT devices in your local network. To do so, it collects information about devices in your
local network and compares them with a database of known devices.

Currently, the following information can be used to fingerprint devices:

* MAC address vendor lookup
* DNS requests
* SSDP broadcasts
* mDNS broadcasts
* Port scanning


## Detect Local Devices

To detect local devices, simply run

    iot_device_id detect



## Record Device Information

To add a new device into the database:

    iot_device_id record --ip 10.0.1.2 --name "Device Name"
    

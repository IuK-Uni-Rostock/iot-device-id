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

## Installation

On Windows, you can use the standalone binary to easily run the graphical user interface. If you want to use 
the command line interface or run it on any other operating system, IoT Device ID can also be installed as 
a Python library.

### Windows Binary

1. Download the latest binary from the [release page](https://github.com/IuK-Uni-Rostock/iot-device-id/releases).
2. Start the downloaded file.

### From Source

1. Install Python 3.5 or higher.
2. From a command line prompt, run `python3 -m pip install git+https://github.com/IuK-Uni-Rostock/iot-device-id[gui]`.
3. Run `iot-device-id` to start the graphical user interface or `iot-device-id-cli` for a command line interface.


## Usage

### Graphical User Interface

Once started, IoT Device ID should start scanning devices in your local network. A list of known devices
with their corresponding IP address will appear. 


#### Save new device

If you want to save the signature of a device into the database, click the "Record Device" button. 

A prompt will ask you for the device's IP address and its name.

The app will now start getting information about your device. You can see the retrieved record type and information
in the table.

To make sure you have all important information, you should restart the target device, if possible.
This usually leads to the device announcing itself in the network and sending DNS queries, which IoT device ID 
registers.


### Command line interface

#### Detect Local Devices

To detect local devices, simply run

    iot-device-id-cli detect



#### Record Device Information

To add a new device into the database:

    iot-device-id-cli record --ip 10.0.1.2 --name "Device Name"
    
The data will be automatically saved into the database. You can shut down the program by pressing `Ctrl`+`c`.
import glob
import json
import logging
import os


class CharacterisableMixin(object):
    def __init__(self):
        self.characteristics = {}

    def add_characteristic(self, name, record):
        if name not in self.characteristics:
            self.characteristics[name] = []
        self.characteristics[name].append(record)


class DeviceType(CharacterisableMixin):
    def __init__(self, name):
        super().__init__()
        self.name = name


class LocalDevice(CharacterisableMixin):
    def __init__(self, ip):
        super().__init__()
        self.ip = ip
        self.device_type = None
        self.characteristics = {}


class DeviceDB(object):
    def __init__(self):
        logging.info("Reading device database...")
        self.devices = self.read_devices()
        logging.info("Successfully loaded {} devices".format(len(self.devices)))

    @staticmethod
    def read_devices():
        here = os.path.dirname(os.path.realpath(__file__))
        devices_location = "{}/../devices".format(here)
        if not os.path.exists(devices_location):
            os.mkdir(devices_location)
        devices = []
        for d in glob.glob("{}/*.json".format(devices_location)):
            with open(d, "r") as f:
                devices.append(json.load(f))
        return devices

    def find_matching_device_types(self, device_type: LocalDevice) -> [(DeviceType, float)]:
        pass

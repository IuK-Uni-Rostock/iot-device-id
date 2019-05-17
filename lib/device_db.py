import glob
import pickle
import logging
import os
import uuid


class CharacterisableMixin(object):
    def __init__(self):
        self.characteristics = set()

    def add_characteristic(self, name, record):
        self.characteristics.add((name, record))


class DeviceType(CharacterisableMixin):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.uuid = str(uuid.uuid4())

    def __str__(self):
        return "DeviceType(name={}, uuid={})".format(self.name, self.uuid)


class LocalDevice(CharacterisableMixin):
    def __init__(self, ip):
        super().__init__()
        self.ip = ip
        self.device_types = []


class DeviceTypeDB(object):
    here = os.path.dirname(os.path.realpath(__file__))
    devices_location = "{}/../devices".format(here)
    db = None

    def __init__(self):
        logging.info("Reading device type database...")
        self.device_types = self.read_device_types()
        logging.info("Successfully loaded {} device types".format(len(self.device_types)))

    @staticmethod
    def read_device_types():
        if not os.path.exists(DeviceTypeDB.devices_location):
            os.mkdir(DeviceTypeDB.devices_location)
        devices = {}
        for d in glob.glob("{}/*".format(DeviceTypeDB.devices_location)):
            with open(d, "rb") as f:
                device = pickle.load(f)
                devices[device.uuid] = device
        return devices

    @staticmethod
    def get_db():
        if DeviceTypeDB.db is None:
            DeviceTypeDB.db = DeviceTypeDB()
        return DeviceTypeDB.db

    def find_matching_device_types(self, local_device: LocalDevice) -> [(float, DeviceType)]:
        """
        Returns the most likely device types ordered by similarity of characteristics with the device.
        Uses the Sørensen–Dice coefficient to quantify the similarity.
        """
        result = []
        for device in self.device_types.values():
            intersection = len(device.characteristics.intersection(local_device.characteristics))
            dice_index = 2 * intersection / (len(device.characteristics) + len(local_device.characteristics))
            result.append((dice_index, device))
        return sorted(result, key=lambda x: x[0])

    def find_matching_device_type(self, local_device: LocalDevice) -> (float, DeviceType):
        return self.find_matching_device_types(local_device)[0]

    def add(self, device_type: DeviceType):
        self.device_types[device_type.uuid] = device_type
        with open("{}/{}".format(self.devices_location, device_type.uuid), "wb") as f:
            pickle.dump(device_type, f)

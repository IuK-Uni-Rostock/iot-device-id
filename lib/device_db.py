import glob
import json
import logging
import os
import uuid

from lib.utils import fuzzy_intersection


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
        return "DeviceType(name={}, uuid={}, characteristics=[{}])".format(
            self.name, self.uuid, len(self.characteristics))

    def serialise(self, f):
        return json.dump({
            "name": self.name,
            "characteristics": list(self.characteristics)
        }, f)

    @staticmethod
    def deserialise(f):
        data = json.load(f)
        dt = DeviceType(data["name"])
        for c in data["characteristics"]:
            assert isinstance(c[0], str) and isinstance(c[1], str)
            dt.add_characteristic(c[0], c[1])
        return dt


class LocalDevice(CharacterisableMixin):
    local_devices = {}

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
            with open(d, "r") as f:
                device = DeviceType.deserialise(f)
                devices[os.path.basename(d)] = device
        return devices

    @staticmethod
    def get_db():
        if DeviceTypeDB.db is None:
            DeviceTypeDB.db = DeviceTypeDB()
        return DeviceTypeDB.db

    def find_matching_device_types(self, local_device: LocalDevice, ignore=tuple()) -> [(float, DeviceType)]:
        """
        Returns the most likely device types ordered by similarity of characteristics with the device.
        Uses the Jaccard index to quantify the similarity.
        """

        result = []
        for device_type in self.device_types.values():

            # E.g. if DNS is not enabled, ignore all DNS records
            dtc = set([c for c in device_type.characteristics if c[0] not in ignore])

            intersection = fuzzy_intersection(dtc, local_device.characteristics)
            union = len(dtc.union(local_device.characteristics))
            jaccard_index = intersection / union
            result.append((jaccard_index, device_type))
        return sorted(result, key=lambda x: x[0], reverse=True)

    def find_matching_device_type(self, local_device: LocalDevice) -> (float, DeviceType):
        return self.find_matching_device_types(local_device)[0]

    def add(self, device_type: DeviceType):
        self.device_types[device_type.uuid] = device_type
        with open("{}/{}".format(self.devices_location, device_type.uuid), "w") as f:
            device_type.serialise(f)

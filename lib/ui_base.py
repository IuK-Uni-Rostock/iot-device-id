# noinspection PyArgumentList
import asyncio
import logging
import re

from lib.device_db import LocalDevice, DeviceTypeDB, DeviceType

from lib.discovery import dns, ssdp, mdns, port_scan, arp, nupnp, ws_discovery


class Mode:
    Record = 1
    Detect = 2


class BaseUI(object):
    listeners = (dns, ssdp, mdns, port_scan, arp, nupnp, ws_discovery)

    def __init__(self):
        self.recording_device_type = None
        self.recording_ip = None
        self.mode = None
        self.listeners_started = False

    def start_listeners(self):
        if self.listeners_started:
            return
        loop = asyncio.get_event_loop()
        for l in BaseUI.listeners:
            loop.create_task(l.start(self))
        self.listeners_started = True
        loop.run_forever()

    @staticmethod
    def _get_disabled_listeners():
        disabled = []
        for l in BaseUI.listeners:
            if not l.enabled:
                disabled.append(l.__name__.split(".")[-1])
        return disabled

    def on_receive(self, remote_ip, type, record):
        if isinstance(remote_ip, bytes):
            remote_ip = remote_ip.decode("utf8")
        if remote_ip not in LocalDevice.local_devices:
            LocalDevice.local_devices[remote_ip] = LocalDevice(remote_ip)
        LocalDevice.local_devices[remote_ip].add_characteristic(type, record)
        if self.mode == Mode.Record:
            if remote_ip != self.recording_ip:
                logging.debug("Ignoring {} record from {} (!= {})".format(type, remote_ip, self.recording_ip))
            else:
                self.recording_device_type.add_characteristic(type, record)
                DeviceTypeDB.get_db().add(self.recording_device_type)
                logging.info(
                    "Saving {} record '{}' for device type {}".format(type, record, self.recording_device_type))
            for c in self.recording_device_type.characteristics:
                self.add_row([c[0], c[1]])
            self.draw()
        if self.mode == Mode.Detect:
            self.sort_by_row(3)
            logging.info("Received {} record '{}' for device at {}".format(type, record, remote_ip))

            LocalDevice.local_devices[remote_ip].device_types = DeviceTypeDB.get_db().find_matching_device_types(
                LocalDevice.local_devices[remote_ip], ignore=BaseUI._get_disabled_listeners())

            logging.info("Local device at {} has characteristics {}, matches {} with {}.".format(
                remote_ip,
                LocalDevice.local_devices[remote_ip].characteristics,
                LocalDevice.local_devices[remote_ip].device_types[0][1].name,
                LocalDevice.local_devices[remote_ip].device_types[0][0] * 100
            ))

            for (ip, ld) in LocalDevice.local_devices.items():
                # If likelihood is > 0
                if len(ld.device_types) and ld.device_types[0][0] > 0:
                    dt = ld.device_types[0]
                    self.add_row([ip, dt[1].name, "{}%".format(int(dt[0] * 100))])
            self.draw()

    def start_recording(self, ip, name):
        self.set_headers(["Type", "Record"])
        self.draw()
        self.mode = Mode.Record
        self.recording_ip = ip
        self.recording_device_type = DeviceType(name)
        if ip not in LocalDevice.local_devices:
            LocalDevice.local_devices[ip] = LocalDevice(ip)
        else:
            for c in LocalDevice.local_devices[ip].characteristics:
                self.recording_device_type.add_characteristic(*c)
        self.start_listeners()

    def start_detecting(self):
        self.mode = Mode.Detect
        self.set_headers(["Local IP address", "Device Type", "Match"])
        self.start_listeners()

    def set_headers(self, headers):
        raise NotImplementedError()

    def add_row(self, values):
        raise NotImplementedError()

    def draw(self):
        raise NotImplementedError()

    def sort_by_row(self, i):
        raise NotImplementedError()

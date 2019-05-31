import asyncio
import logging
import sys

import click

from lib.discovery import ssdp, dns, mdns, arp, port_scan
from lib.device_db import DeviceType, DeviceTypeDB, LocalDevice
from lib.utils import LogStream, TexttableWithLogStream

log_stream = LogStream()
logging.basicConfig(level=logging.DEBUG, stream=log_stream, format="%(asctime)s;%(levelname)s;%(message)s")


def start_listeners(on_receive):
    if sys.platform == 'win32':
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
    else:
        loop = asyncio.get_event_loop()
    loop.create_task(dns.start(on_receive))
    loop.create_task(ssdp.start(on_receive))
    loop.create_task(mdns.start(on_receive))
    loop.create_task(port_scan.start(on_receive))
    loop.create_task(arp.start(on_receive))

    loop.run_forever()


@click.group()
def cli():
    pass


@click.command()
@click.option("--ip", help="IP address of target device", prompt="Target IP address")
@click.option("--name", prompt="Device name", help="Name of the target device")
def record(ip, name):
    """Record a new device into the database."""
    device_type = DeviceType(name)
    LocalDevice.local_devices[ip] = LocalDevice(ip)

    def on_receive(remote_ip, type, record):
        t = TexttableWithLogStream(log_stream, ["", "Type", "Record"])
        if isinstance(remote_ip, bytes):
            remote_ip = remote_ip.decode("utf8")
        if remote_ip != ip:
            logging.debug("Ignoring {} record from {} (!= {})".format(type, remote_ip, ip))
        else:
            device_type.add_characteristic(type, record)
            DeviceTypeDB.get_db().add(device_type)
            logging.info("Saving {} record '{}' for device type {}".format(type, record, device_type))
        for i, c in enumerate(device_type.characteristics):
            t.add_row([i+1, c[0], c[1]])
        t.draw()

    start_listeners(on_receive)


@click.command()
def detect():
    """Detect IoT devices on the local network."""
    def on_receive(remote_ip, type, record):
        if isinstance(remote_ip, bytes):
            remote_ip = remote_ip.decode("utf8")
        logging.info("Received {} record '{}' for device at {}".format(type, record, remote_ip))
        t = TexttableWithLogStream(log_stream, ["", "Local IP address", "Device Type", "Match"])
        if remote_ip not in LocalDevice.local_devices:
            LocalDevice.local_devices[remote_ip] = LocalDevice(remote_ip)
        LocalDevice.local_devices[remote_ip].add_characteristic(type, record)
        LocalDevice.local_devices[remote_ip].device_types = DeviceTypeDB.get_db().find_matching_device_types(LocalDevice.local_devices[remote_ip])

        for i, (ip, ld) in enumerate(LocalDevice.local_devices.items()):
            # If likelihood is > 0
            if len(ld.device_types) and ld.device_types[0][0] > 0:
                dt = ld.device_types[0]
                t.add_row(["#{}".format(i+1), ip, dt[1], "{}%".format(int(dt[0] * 100))])
        t.draw()
    start_listeners(on_receive)


cli.add_command(record)
cli.add_command(detect)

if __name__ == '__main__':
    cli()

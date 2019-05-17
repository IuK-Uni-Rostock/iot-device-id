import asyncio
import logging
import shutil

import click
from texttable import Texttable

from lib import dns_intercept, ssdp_discovery
from lib.device_db import DeviceType, DeviceTypeDB, LocalDevice

logging.basicConfig(level=logging.DEBUG)


def start_listeners(on_receive):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(dns_intercept.start(on_receive))
    loop.run_until_complete(ssdp_discovery.start(loop, on_receive))

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

    def on_receive(remote_ip, type, record):
        if remote_ip != ip:
            logging.debug("Ignoring request from {} (!= {})".format(remote_ip, ip))
            return
        device_type.add_characteristic(type, record)
        DeviceTypeDB.get_db().add(device_type)
        logging.info("Saving {} record '{}' for device type {}".format(type, record, device_type))

    start_listeners(on_receive)


@click.command()
def detect():
    """Detect IoT devices on the local network."""
    local_devices = {}
    t = Texttable()
    t.set_max_width(shutil.get_terminal_size((80, 20)).columns)

    def on_receive(remote_ip, type, record):
        if remote_ip not in local_devices:
            local_devices[remote_ip] = LocalDevice(remote_ip)
        local_devices[remote_ip].add_characteristic(type, record)
        local_devices[remote_ip].device_types = DeviceTypeDB.get_db().find_matching_device_types(local_devices[remote_ip])
        t.reset()
        click.clear()
        t.header(["", "Local IP address", "Device Type", "Certainty"])
        for i, (ip, ld) in enumerate(local_devices.items()):
            dt = ld.device_types[0] if len(ld.device_types) else (0.0, "Unknown")
            t.add_row(["#{}".format(i+1), ip, dt[1], "{}% likely".format(int(dt[0] * 100))])
        print(t.draw())
    start_listeners(on_receive)


cli.add_command(record)
cli.add_command(detect)

if __name__ == '__main__':
    cli()

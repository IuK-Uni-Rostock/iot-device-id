import asyncio
import logging
import shutil

import click
from texttable import Texttable

from lib.discovery import ssdp, dns, mdns, arp
from lib.device_db import DeviceType, DeviceTypeDB, LocalDevice
from lib.utils import LogStream


log_stream = LogStream()
logging.basicConfig(level=logging.DEBUG, stream=log_stream, format="%(asctime)s;%(levelname)s;%(message)s")


def start_listeners(on_receive):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(dns.start(on_receive))
    loop.run_until_complete(ssdp.start(on_receive))
    loop.run_until_complete(mdns.start(on_receive))
    loop.run_until_complete(arp.start(on_receive))

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

    def on_receive(remote_ip, type, record):
        tsize = shutil.get_terminal_size((80, 20))
        t = Texttable()
        t.set_max_width(tsize.columns)
        if remote_ip not in local_devices:
            local_devices[remote_ip] = LocalDevice(remote_ip)
        local_devices[remote_ip].add_characteristic(type, record)
        local_devices[remote_ip].device_types = DeviceTypeDB.get_db().find_matching_device_types(local_devices[remote_ip])
        click.clear()
        t.header(["", "Local IP address", "Device Type", "Match"])
        for i, (ip, ld) in enumerate(local_devices.items()):
            # If likelihood is > 0
            if len(ld.device_types) and ld.device_types[0][0] > 0:
                dt = ld.device_types[0]
                t.add_row(["#{}".format(i+1), ip, dt[1], "{}%".format(int(dt[0] * 100))])
        print(t.draw())
        print("\n" * (tsize.lines - len(t.draw().splitlines()) - 13))
        print("Log:")
        print(log_stream)
    start_listeners(on_receive)


cli.add_command(record)
cli.add_command(detect)

if __name__ == '__main__':
    cli()

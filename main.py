import asyncio
import logging

import click

from lib import dns_intercept, ssdp_discovery
from lib.device_db import DeviceType, DeviceTypeDB

logging.basicConfig(level=logging.DEBUG)


def start_listeners(on_receive= lambda *_: None):
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
            return
        device_type.add_characteristic(type, record)
        DeviceTypeDB.get_db().add(device_type)
        logging.info("Saving {} record '{}' for device type {}".format(type, record, device_type))

    start_listeners(on_receive=on_receive)


@click.command()
def detect():
    """Detect IoT devices on the local network."""
    start_listeners()


cli.add_command(record)
cli.add_command(detect)

if __name__ == '__main__':
    cli()

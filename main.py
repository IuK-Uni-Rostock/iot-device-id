import asyncio
import logging

import click

from lib import dns_intercept, ssdp_discovery

logging.basicConfig(level=logging.DEBUG)


def start_listeners():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(dns_intercept.start())
    loop.run_until_complete(ssdp_discovery.start(loop))

    loop.run_forever()


@click.group()
def cli():
    pass


@click.command()
@click.option("--ip", help="IP address of target device", prompt="Target IP address")
@click.option("--name", prompt="Device name", help="Name of the target device")
def record(ip, name):
    """Record a new device into the database."""
    print(ip, name)
    start_listeners()


@click.command()
def detect():
    """Detect IoT devices on the local network."""
    start_listeners()


cli.add_command(record)
cli.add_command(detect)

if __name__ == '__main__':
    cli()

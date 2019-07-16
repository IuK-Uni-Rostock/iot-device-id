import logging
import os

import click

from lib.ui_base import BaseUI
from lib.utils import TexttableWithLogStream, LogStream


if "LOG_FILE" in os.environ:
    log_file = os.environ["LOG_FILE"]
else:
    log_file = "iot-device-id.log"

log_stream = LogStream()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(log_stream)
    ])


class ConsoleUI(BaseUI):
    def __init__(self):
        super().__init__()
        self.tt = None
        self.rows = []
        self.sort_by = 0

    def set_headers(self, headers):
        self.tt = TexttableWithLogStream(log_stream, headers)

    def sort_by_row(self, i):
        self.sort_by = i

    def add_row(self, values):
        self.rows.append(values)

    def draw(self):
        rows = self.rows
        self.rows = []
        for v in rows:
            self.tt.add_row(v)
        self.tt.draw()

    def record(self, ip, name):
        """Record a new device into the database."""
        self.start_recording(ip, name)

    def detect(self):
        """Detect IoT devices on the local network."""
        self.start_detecting()


@click.group()
def cli():
    pass


@click.command()
@click.option("--ip", help="IP address of target device", prompt="Target IP address")
@click.option("--name", prompt="Device name", help="Name of the target device")
def record(ip, name):
    ConsoleUI().record(ip, name)


@click.command()
def detect():
    ConsoleUI().detect()


cli.add_command(record)
cli.add_command(detect)

if __name__ == '__main__':
    cli()

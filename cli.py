import click

from lib.ui_base import BaseUI, log_stream
from lib.utils import TexttableWithLogStream


class ConsoleUI(BaseUI):
    def __init__(self):
        super().__init__()
        self.tt = None

    def set_headers(self, headers):
        self.tt = TexttableWithLogStream(log_stream, headers)

    def add_row(self, values):
        self.tt.add_row(values)

    def draw(self):
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

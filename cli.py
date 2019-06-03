import click

from lib.ui_base import BaseUI, log_stream
from lib.utils import TexttableWithLogStream


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
        rows = sorted(self.rows, key=lambda x: int(x[self.sort_by][:-1]), reverse=True)
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

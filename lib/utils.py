import asyncio
import os
import re
import shutil
import subprocess
from collections import deque

import click
from texttable import Texttable
from fuzzywuzzy import process



async def get_arp_table():
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _get_arp_table_sync)


def _get_arp_table_sync():
    if os.name == "nt":
        switch, drop_param = "-a", 2
    else:
        switch, drop_param = "-e", 1
    arp_table = subprocess.check_output(["arp", switch])
    arp_table = [l.split()[:3] for l in arp_table.splitlines() if len(l)]
    for elem in arp_table:
        elem.pop(drop_param)
    arp_table = [elem for elem in arp_table if validate_mac(elem[1])]
    return arp_table


def validate_mac(mac):
    return re.match(b'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$', mac)


class LogStream(object):
    def __init__(self):
        self.logs = deque(maxlen=15)

    def write(self, str):
        self.logs.append(str)

    def flush(self):
        pass

    def __str__(self):
        return "".join(self.logs)


class TexttableWithLogStream(object):
    def __init__(self, log_stream, headers):
        self.log_stream = log_stream
        self.headers = headers
        self.t = Texttable()
        self.t.header(self.headers)

    def add_row(self, items):
        self.t.add_row(items)

    def draw(self):
        click.clear()
        tsize = shutil.get_terminal_size((80, 20))
        self.t.set_max_width(tsize.columns)
        print(self.t.draw())
        print("\n" * (tsize.lines - len(self.t.draw().splitlines()) - 13))
        print("Log:")
        print(self.log_stream)
        self.t = Texttable()
        self.t.header(self.headers)


def fuzzy_intersection(a, b):
    return sum([process.extractOne(i, b)[1]/100 for i in a])

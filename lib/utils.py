import asyncio
import os
import re
from asyncio.subprocess import create_subprocess_exec
from collections import deque


async def get_arp_table():
    if os.name == "nt":
        switch, drop_param = "-a", 2
    else:
        switch, drop_param = "-e", 1
    proc = await create_subprocess_exec("arp", switch, stdout=asyncio.subprocess.PIPE)
    await proc.wait()
    arp_table = (await proc.stdout.read())
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

import asyncio
import subprocess

import pytest

from lib.dns_intercept import start


class Receiver:
    def __init__(self):
        self.events = []

    def on_receive(self, *args):
        self.events.append(args)


@pytest.mark.asyncio
async def test_dns():
    r = Receiver()
    await start(r.on_receive, port=5353)
    proc = await asyncio.create_subprocess_shell(" ".join(["dig", "-p", "5353", "@localhost", "google.com", "A"]))
    await proc.wait()
    assert len(r.events) == 1
    assert r.events[0][1] == 'DNS'
    assert r.events[0][2] == "('google.com', 'A')"

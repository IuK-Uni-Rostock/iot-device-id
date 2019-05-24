import asyncio

import pytest

from lib.discovery.dns import start


class Receiver:
    def __init__(self):
        self.events = []

    def on_receive(self, *args):
        self.events.append(args)


@pytest.mark.asyncio
async def test_dns():
    r = Receiver()
    await start(r.on_receive, port=5300)
    proc = await asyncio.create_subprocess_shell(" ".join(["dig", "-p", "5300", "@localhost", "google.com", "A"]))
    await proc.wait()
    assert len(r.events) == 1
    assert r.events[0][1] == 'DNS'
    assert r.events[0][2] == "('google.com', 'A')"

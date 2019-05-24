import pytest

from lib.discovery.ssdp import start
from tests.test_dns import Receiver


@pytest.mark.asyncio
async def test_ssdp():
    r = Receiver()
    await start(r.on_receive)


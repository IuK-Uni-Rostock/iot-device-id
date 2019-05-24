import pytest

from lib.discovery.mdns import start
from tests.test_dns import Receiver


@pytest.mark.asyncio
async def test_mdns():
    r = Receiver()
    await start(r.on_receive)


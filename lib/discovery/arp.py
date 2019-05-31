import asyncio
import logging

from mac_vendor_lookup import AsyncMacLookup

from lib.utils import get_arp_table


async def start(on_receive):
    mac = AsyncMacLookup()
    while True:
        arp_table = await get_arp_table()
        for elem in arp_table:
            try:
                vendor = await mac.lookup(elem[1])
                on_receive(elem[0], "Vendor", vendor)
            except KeyError:
                pass
        await asyncio.sleep(30)


if __name__ == "__main__":
    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start(None))

import asyncio

from mac_vendor_lookup import AsyncMacLookup

from lib.utils import get_arp_table


async def start(parent):
    mac = AsyncMacLookup()
    while True:
        arp_table = await get_arp_table()
        for elem in arp_table:
            try:
                vendor = await mac.lookup(elem[1])
                parent.on_receive(elem[0], "Vendor", vendor)
            except KeyError:
                pass
        await asyncio.sleep(30)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start(None))

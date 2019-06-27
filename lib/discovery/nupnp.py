import asyncio

import aiohttp

enabled = True


ENDPOINTS = [
    "https://nupnp.com/api/devices",
    "https://discovery.meethue.com/"
             ]


async def start(parent):
    while True:
        for e in ENDPOINTS:
            clients = await get_json(e)
            for c in clients:
                ip = c["internaladdress"]
                name = c["name"]
                parent.on_receive(ip, "NUPNP", name)
        await asyncio.sleep(60 * 60)


async def get_json(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()

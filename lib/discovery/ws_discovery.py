import asyncio

from wsdiscovery import WSDiscovery

enabled = True


async def start(parent):
    loop = asyncio.get_event_loop()
    wsd = WSDiscovery()
    await loop.run_in_executor(None, wsd.start)
    while True:
        services = await loop.run_in_executor(None, wsd.searchServices)
        for service in services:
            ip = service.getXAddrs()[0].split("/")[2].rsplit(":", 1)[0]
            record = "{},{}".format(service.getScopes(), service.getTypes())
            parent.on_receive(ip, "WS-Discovery", record)

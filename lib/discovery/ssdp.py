import asyncio
import socket
import logging

import ssdp


async def start(parent):
    class MyProtocol(ssdp.SimpleServiceDiscoveryProtocol):

        def response_received(self, response, addr):
            parent.on_receive(addr, "SSDP", response)

        def request_received(self, request, addr):
            logging.debug("SSDP Request for {} from {}".format(request, addr))

    loop = asyncio.get_event_loop()
    transport, protocol = await loop.create_datagram_endpoint(MyProtocol, family=socket.AF_INET)
    logging.debug("Listening for SSDP announcements")

    notify = ssdp.SSDPRequest('M-SEARCH', headers=[("ST", "ssdp:all"), ("MAN", "ssdp:discover")])
    notify.sendto(transport, (MyProtocol.MULTICAST_ADDRESS, 1982))

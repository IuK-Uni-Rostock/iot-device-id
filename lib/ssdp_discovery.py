import socket
import logging

import ssdp


class MyProtocol(ssdp.SimpleServiceDiscoveryProtocol):

    def response_received(self, response, addr):
        print(response, addr)

    def request_received(self, request, addr):
        print(request, addr)


async def start(loop):
    transport, protocol = await loop.create_datagram_endpoint(MyProtocol, family=socket.AF_INET)
    logging.debug("Listening for SSDP announcements")

    notify = ssdp.SSDPRequest('NOTIFY')
    notify.sendto(transport, (MyProtocol.MULTICAST_ADDRESS, 1982))

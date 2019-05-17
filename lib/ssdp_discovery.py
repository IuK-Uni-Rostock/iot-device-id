import socket
import logging

import ssdp


async def start(loop, on_receive):
    class MyProtocol(ssdp.SimpleServiceDiscoveryProtocol):

        def response_received(self, response, addr):
            on_receive(addr, "SSDP", response)
            logging.debug("SSDP Response for {} from {}".format(response, addr))

        def request_received(self, request, addr):
            logging.debug("SSDP Request for {} from {}".format(request, addr))

    transport, protocol = await loop.create_datagram_endpoint(MyProtocol, family=socket.AF_INET)
    logging.debug("Listening for SSDP announcements")

    notify = ssdp.SSDPRequest('NOTIFY')
    notify.sendto(transport, (MyProtocol.MULTICAST_ADDRESS, 1982))

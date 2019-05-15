import logging

from async_dns import DNSMessage
from async_dns.server import DNSProtocol, DNSMixIn, DNSDatagramProtocol, DNSServer


class OurDNSMixIn(DNSMixIn):

    async def handle(self, data, addr):
        msg = DNSMessage.parse(data)
        logging.debug("Request for {} from {}".format(msg.qd, addr))

        # Send a response:
        await super().handle(data, addr)


class OurDNSProtocol(OurDNSMixIn, DNSProtocol):
    pass


class OurDNSDatagramProtocol(OurDNSMixIn, DNSDatagramProtocol):
    pass


server = DNSServer(protocol_classes=(OurDNSProtocol, OurDNSDatagramProtocol))


async def start():
    tcpserver, udptransport = await server.start_server()

    if tcpserver:
        logging.debug("DNS server listening on 0.0.0.0 port 53/tcp")
    if udptransport:
        logging.debug("DNS server listening on 0.0.0.0 port 53/udp")
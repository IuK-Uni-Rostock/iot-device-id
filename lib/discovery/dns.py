import logging

from async_dns import DNSMessage
from async_dns.server import DNSProtocol, DNSMixIn, DNSDatagramProtocol, DNSServer


async def start(on_receive, port=53):
    class OurDNSMixIn(DNSMixIn):

        async def handle(self, data, addr):
            msg = DNSMessage.parse(data)
            logging.debug("DNS Request for {} from {}".format(msg.qd, addr))
            on_receive(addr[0], "DNS", str(msg.qd[0]))

            # Send a response:
            await super().handle(data, addr)

    class OurDNSProtocol(OurDNSMixIn, DNSProtocol):
        pass

    class OurDNSDatagramProtocol(OurDNSMixIn, DNSDatagramProtocol):
        pass

    server = DNSServer(protocol_classes=(OurDNSProtocol, OurDNSDatagramProtocol), port=port)

    tcpserver, udptransport = await server.start_server()

    if tcpserver:
        logging.debug("DNS server listening on 0.0.0.0 port 53/tcp")
    if udptransport:
        logging.debug("DNS server listening on 0.0.0.0 port 53/udp")

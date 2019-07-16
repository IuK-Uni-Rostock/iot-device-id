import logging

from async_dns import DNSMessage
from async_dns.server import DNSProtocol, DNSMixIn, DNSDatagramProtocol, DNSServer

enabled = False

logging.getLogger("async_dns").setLevel(logging.CRITICAL)


async def start(parent, port=53):
    global enabled

    class OurDNSMixIn(DNSMixIn):

        async def handle(self, data, addr):
            msg = DNSMessage.parse(data)
            parent.on_receive(addr[0], "DNS", str(msg.qd[0]))

            # Send a response:
            try:
                await super().handle(data, addr)
            except TypeError:
                pass

    class OurDNSProtocol(OurDNSMixIn, DNSProtocol):
        pass

    class OurDNSDatagramProtocol(OurDNSMixIn, DNSDatagramProtocol):
        pass

    server = DNSServer(protocol_classes=(OurDNSProtocol, OurDNSDatagramProtocol), port=port)

    try:
        tcp_server, udp_transport = await server.start_server()
        if tcp_server:
            logging.debug("DNS server listening on 0.0.0.0 port 53/tcp")
            enabled = True
        if udp_transport:
            logging.debug("DNS server listening on 0.0.0.0 port 53/udp")
    except PermissionError as e:
        logging.error("Unable to start DNS server on port 53. Permission denied: {}".format(e))

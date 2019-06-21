import socket
import struct
import logging

SSDP_BROADCAST_PORT = 1900
SSDP_BROADCAST_ADDR = "239.255.255.250"


async def start(loop, on_receive):
    class SSDPProtocol(object):
        bad_prefixes = ["uuid:"]
        bad_fields = ["LOCATION", "HOST", "CACHE-CONTROL"]

        # noinspection PyMethodMayBeStatic
        def datagram_received(self, data, addr):
            fields = [v.split(": ") for v in data.decode("utf8").splitlines()]
            method, fields = fields[0][0], fields[1:]
            fields = [v for v in fields if len(v) > 1 and not v[1].startswith("uuid:")]
            for item in fields:
                on_receive(addr[0], "SSDP", "{}: {}".format(method, item))

    addrinfo = socket.getaddrinfo(SSDP_BROADCAST_ADDR, None)[0]
    sock = socket.socket(addrinfo[0], socket.SOCK_DGRAM)
    group_bin = socket.inet_pton(addrinfo[0], addrinfo[4][0])
    sock.bind(('', SSDP_BROADCAST_PORT))
    mreq = group_bin + struct.pack('=I', socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    await loop.create_datagram_endpoint(SSDPProtocol, sock=sock)
    logging.debug("Listening for SSDP announcements")

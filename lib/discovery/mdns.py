import asyncio

from aiozeroconf import ServiceBrowser, Zeroconf
import aiozeroconf

enabled = True


async def start(parent):
    class DummyListener(object):

        def add_service(self, *_):
            pass

    class MyMCListener(aiozeroconf.aiozeroconf.MCListener):
        def datagram_received(self, data, addrs):
            super().datagram_received(data, addrs)
            msg = aiozeroconf.aiozeroconf.DNSIncoming(data)
            for a in msg.answers:
                typ = str(a).split(",")[-1][:-1]
                src_addr = addrs[0]
                parent.on_receive(src_addr, "mDNS", typ)

    # Monkey-patch aiozeroconf so we have access to the source IP
    aiozeroconf.aiozeroconf.MCListener = MyMCListener
    loop = asyncio.get_event_loop()
    zeroconf = Zeroconf(loop)
    listener = DummyListener()
    ServiceBrowser(zeroconf, "_services._dns-sd._udp.local.", listener)

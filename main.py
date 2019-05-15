import asyncio
import logging

from lib import dns_intercept, ssdp_discovery

logging.basicConfig(level=logging.DEBUG)

loop = asyncio.get_event_loop()
loop.run_until_complete(dns_intercept.start())
# loop.run_until_complete(ssdp_discovery.start(loop))

loop.run_forever()

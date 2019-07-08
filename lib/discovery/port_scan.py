import asyncio
import copy
import logging

from lib.device_db import LocalDevice

ports = (80, 443,  # HTTP
         22,  # SSH
         1883,  # MQTT
         1900,  # UPNP
         )

enabled = True


async def check_port(ip, port):
    loop = asyncio.get_event_loop()
    conn = asyncio.open_connection(ip, port, loop=loop)
    try:
        await asyncio.wait_for(conn, timeout=1)
        return True
    except:
        return False


async def start(parent):
    while True:
        # Wait for other services to find probable devices
        await asyncio.sleep(2)
        logging.info("Scanning {} devices".format(LocalDevice.local_devices))
        for ip, _ in list(LocalDevice.local_devices.items()):
            logging.info("Scanning {}".format(ip))
            for p in ports:
                if await check_port(ip, p):
                    parent.on_receive(ip, "open port", "tcp/{}".format(p))
                await asyncio.sleep(0.5)
        await asyncio.sleep(60)

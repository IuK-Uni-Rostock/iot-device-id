import asyncio
import logging, traceback, socket

from lib.device_db import LocalDevice

ports = (80, 443,  # HTTP
         22,  # SSH
         1883,  # MQTT
         1900,  # UPNP
         )

enabled = True


async def check_port(ip, port):
    loop = asyncio.get_event_loop()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.settimeout(1)
    conn = asyncio.open_connection(ip, port, loop=loop)
    try:
        await asyncio.wait_for(loop.run_in_executor(None, lambda: sock.connect((ip, port))), 1, loop=loop)
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
        await asyncio.sleep(20)

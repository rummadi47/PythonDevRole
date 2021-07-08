#!/usr/bin/python

# Author: @Saritha Ummadi
# Usage:
#   python pingdiscover --subnet "192.168.0.0/24" --concurrent 8 --timeout 2
#

from argparse import ArgumentParser

import asyncio
import ipaddress
from aioping import verbose_ping, ping
import logging
import socket



class Aioping():
    def __init__(self):
        #-- Logging Enabled
        logging.basicConfig(level=logging.INFO)
        #-- Default Semaphore
        self.semaphore = asyncio.Semaphore(20)
    
    def set_semaphore(self, concurrency_level):
        """Semaphore sets no of concurrent processes"""
        self.semaphore = asyncio.Semaphore(int(concurrency_level))

    async def _do_ping(self, host, timeout=5):
        """do_ping pings the network"""
        try:
            #-- Semaphore for concurrent processes 
            async with self.semaphore:
                # socket.AddressFamily.AF_INET - Denotes IPV4 addresses only, and will ignore IPV6 addresses
                delay = await verbose_ping(host, family=socket.AddressFamily.AF_INET,  timeout=timeout) * 1000
                print(f"{host} ping response in {delay:0.4f}ms")
                return delay
        except TimeoutError:
            print("%s timed out" % host)
        except Exception as e:
                pass

    def ping_discover(self, subnet="192.168.0.0/24", timeout="5"):
        try:
            timeout = int(timeout)
        except Exception:
            print("Invalid Timeout or Concurrent Level")
            return False
        
        try:
            # network = ipaddress.IPv4Network(subnet) #-- Only for IPV4network
            network = ipaddress.ip_network(subnet, strict=False) #1.1 #-- Work for IPV6 and IPV4 too
        except ValueError:
            print('address/netmask is invalid for IPv4:', subnet)
            return False
        loop = asyncio.get_event_loop()
        
        tasks = []
        for index, ip in enumerate(network.hosts()):
            tasks.append(asyncio.ensure_future(self._do_ping(f"{ip}",  timeout=timeout)))

        loop.run_until_complete(asyncio.gather(*tasks))

    def main(self):
        parser = ArgumentParser()
        parser.add_argument("-s", "--subnet", dest="subnet", required=True,
                            help="Subnet + Netmask  eg. 192.168.0.0/24")
        parser.add_argument("-c", "--concurrent", dest="concurrency_level",
                            help="Concurrency Level, Number of concurrent hosts that are pinged at the same time")
        parser.add_argument("-t", "--timeout", dest="timeout", default="5",
                            help="The number of seconds after giving up on pinging a host")
        self.args = parser.parse_args()



if __name__ == '__main__':
    # pingdiscover -s "192.168.0.0/24" --concurrent 8 --timeout 2
    # ping('google.com', timeout=3000, count=3, delay=0.5, verbose=True)
    print("Initiating script....")
    aiping = Aioping()
    aiping.main()
    aiping.set_semaphore(aiping.args.concurrency_level)
    print("Arguments", aiping.args)
    aiping.ping_discover(subnet=aiping.args.subnet, timeout=aiping.args.timeout)
    print("Run completed script....")

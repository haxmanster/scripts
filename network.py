#!/usr/bin/python3

# all code in this file is very weak, it's not production, just lab
from libs import *

import platform
import configparser

# check if Ubuntu 18.04
# FIXME change method to other not deprecated
if platform.linux_distribution()[2] != "bionic":
    exit("This scripts supports only Ubuntu 18.04, sorry! :(")

# check root
if os.geteuid() != 0:
    exit("You need to run this as a root!")

# parse configuration file, exit and inform user if we don't have config
config = configparser.ConfigParser()
config.read('config.ini')
if "Network" not in config:
    print("Please copy and edit config first:")
    print("    cp config.example.ini config.ini")
    exit(1)

# check if all config variables are set
conf_is_wrong = False
conf_variables = ["IpEnd", "NetFlowHost", "SflowHost", "DpdkIface", "Mask"]
for var in conf_variables:
    if var not in config["Network"]:
        print(f"Please add \"{var}\" to config.ini")
        conf_is_wrong = True
# exit if we don't have all needed variables in config
if conf_is_wrong:
    print("See config.example.ini for more information")
    exit(1)

# check if packages are installed, install all stuff we need
# https://stackoverflow.com/a/3391589
devnull = open(os.devnull, "w")
retval = subprocess.call(["dpkg", "-s", "nload"], stdout=devnull, stderr=subprocess.STDOUT)
devnull.close()
if retval != 0:
    print("Required packages probably not installed, installing...")
    run(
        "apt-get update && apt-get install -y bridge-utils openvswitch-switch openvswitch-switch-dpdk nload iftop hugepages"
    )

# real work incoming! finally...
print("Detected interfaces:")
print(get_interfaces())
interfaces = get_interfaces()
os_deps()
ip_end = config["Network"]["IpEnd"]
netflow_addr = config["Network"]["NetFlowHost"]
sflow_addr = config["Network"]["SflowHost"]
mask = config["Network"]["Mask"]
create_br(0, netflow_addr, sflow_addr)
create_net(0, "192.168.1", ip_end, mask)
create_ns(1, "10.10.10", ip_end, 100, 0, mask)
create_ns(2, "10.10.10", ip_end, 100, 0, mask)
create_ns(3, "10.10.10", ip_end, 200, 0, mask)
create_ns(4, "10.10.10", ip_end, 200, 0, mask)
create_ns(5, "10.10.10", ip_end, 300, 0, mask)
# use pci addr for card defined in config
for card in interfaces:
    if card["new"] == config["Network"]["DpdkIface"]:
        dpdk_conf(card["pci_addr"], 1, ip_end)

print("###")
autostart()
print("###")
print("Ready! Enjoy")

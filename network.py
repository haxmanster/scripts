#!/usr/bin/python3

import os
import platform
import subprocess
import configparser


# define all tools #

def log(s):
    print(s)


def quiet_exec(cmd):
    os.system(cmd + " > /dev/null 2>&1")


def os_deps():
    quiet_exec("modprobe 8021q && echo 1 > /proc/sys/net/ipv4/ip_forward")


def create_br(br_id, openflow_addr):
    log(f"Creating bridge br{br_id} with OpenFlow controller @ {openflow_addr}")
    # openvswitch bridge create and info
    quiet_exec(f"ovs-vsctl add-br br{br_id}")
    quiet_exec(f"ovs-vsctl set bridge br{br_id} protocols=OpenFlow13")
    # ovs-appctl bridge/dump-flows br0
    quiet_exec(f"ovs-vsctl set-controller br0 tcp:{openflow_addr}")
    # ovs-vsctl show


def create_ns(ns_id, ip_prefix, ip_postfix, vlan_tag, br_id, mask):
    log(f"Creating namespace{ns_id} {ip_prefix}.{ip_postfix}/{mask}")
    # add namespace
    quiet_exec(f"ip netns add namespace{ns_id}")
    # add virtual ethernet cable with two ends
    quiet_exec(f"ip link add vns{ns_id} type veth peer name vpeerns{ns_id}")
    # set virutal ethernet on to belong in namespace1
    quiet_exec(f"ip link set vpeerns{ns_id} netns namespace{ns_id}")
    # show link info from the namespace
    # ip netns exec namespace1 ip link
    # start veth port
    quiet_exec(f"ip link set vns{ns_id} up")
    # add network config to veth in namespace end
    quiet_exec(f"ip netns exec namespace{ns_id} ip addr add {ip_prefix}.{ip_postfix}/24 dev vpeerns{ns_id}")
    # change MTU to prevent problems with VXLAN tunneling
    quiet_exec(f"ip netns exec namespace{ns_id} ip link set mtu 1450 dev vpeerns{ns_id}")
    # it's alive!
    quiet_exec(f"ip netns exec namespace{ns_id} ip link set vpeerns{ns_id} up")
    # add loopback just in case
    quiet_exec(f"ip netns exec namespace{ns_id} ip link set dev lo up")
    # connect second end of veth to switch
    quiet_exec(f"ovs-vsctl add-port br{br_id} vns{ns_id}")
    # tag this veth cable to use only vlan100
    quiet_exec(f"ovs-vsctl set port vns{ns_id} tag={vlan_tag}")


def create_net(net_id, ip_prefix, ip_postfix, mask):
    log(f"Creating net{net_id} {ip_prefix}.{ip_postfix}/{mask}")
    quiet_exec(f"ip link add net{net_id} type veth peer name netpeer{net_id}")
    quiet_exec(f"ip link set net{net_id} up")
    quiet_exec(f"ip addr add {ip_prefix}.{ip_postfix}/24 dev netpeer{net_id}")
    quiet_exec(f"ip link set mtu 1450 dev netpeer{net_id}")
    quiet_exec(f"ip link set netpeer{net_id} up")
    quiet_exec(f"ip ovs-vsctl add-port br0 net{net_id}")


def get_interfaces():
    interface_names = []
    proc = subprocess.Popen("dmesg | grep eth | grep renamed", shell=True, stdout=subprocess.PIPE)
    for line in proc.stdout:
        cmd_split_first = str(line).replace("\\n'", "").strip().split(": renamed from ")
        eth_num = cmd_split_first[1]
        cmd_split_second = cmd_split_first[0].split(" ")
        ens_num = cmd_split_second[-1]
        interface_names.append({"old": eth_num, "new": ens_num})
    return interface_names


def dpdk_conf(iface_id):
    os.system('sysctl -w vm.nr_hugepages=256')
    if 'nr_hugepages' not in open('/etc/sysctl.conf').read():
        os.system('echo "vm.nr_hugepages=256" >> /etc/sysctl.conf')
    quiet_exec('echo "NR_2M_PAGES=640" > /etc/dpdk/dpdk.conf')
    os.system('echo "options vfio enable_unsafe_noiommu_mode=1" > /etc/modprobe.d/vfio-noiommu.conf')
    os.system(f"echo 'pci 0000:00:0{iface_id}.0 vfio-pci' > /etc/dpdk/interfaces")
    # use openvswitch version with DPDK after reboot
    quiet_exec("update-alternatives --set ovs-vswitchd /usr/lib/openvswitch-switch-dpdk/ovs-vswitchd-dpdk")

    # check this first:
    # ovs-vsctl --no-wait set Open_vSwitch . other_config:dpdk-init=true
    # ovs-vsctl add-br br1 -- set bridge br1 datapath_type=netdev
    # ovs-vsctl add-port br1 dpdk-p1 -- set Interface dpdk-p1 type=dpdk options:dpdk-devargs=0000:00:04.0


# main flow start #

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
conf_variables = ["IpEnd", "NetFlowHost", "DpdkIface", "Mask"]
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
    os.system(
        "apt-get update && apt-get install -y bridge-utils openvswitch-switch openvswitch-switch-dpdk dpdk-dev libdpdk-dev nload iftop"
    )

# real work incoming! finally...
print("Detected interfaces:")
print(get_interfaces())
os_deps()
ip_end = config["Network"]["IpEnd"]
netflow_addr = config["Network"]["NetFlowHost"]
mask = config["Network"]["Mask"]
create_br(0, netflow_addr)
create_net(0, "192.168.0", ip_end, mask)
create_ns(1, "10.10.10", ip_end, 100, 0, mask)
create_ns(2, "10.10.10", ip_end, 100, 0, mask)
create_ns(3, "10.10.10", ip_end, 200, 0, mask)
create_ns(4, "10.10.10", ip_end, 200, 0, mask)
create_ns(5, "10.10.10", ip_end, 300, 0, mask)
dpdk_conf(config["Network"]["DpdkIface"].replace("ens", ""))
print("Finished! Enjoy")

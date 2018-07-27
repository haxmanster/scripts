import os
import subprocess
import socket
from pathlib import Path


def log(s):
    print("\n\n# " + s)


def quiet_exec(cmd):
    print(cmd)
    os.system(cmd + " > /dev/null 2>&1")


def run(cmd):
    print(cmd)
    os.system(cmd)


def os_deps():
    quiet_exec("modprobe 8021q && echo 1 > /proc/sys/net/ipv4/ip_forward")


def create_br(br_id, openflow_addr, sflow_addr):
    log(f"Creating bridge br{br_id} with OpenFlow controller @ {openflow_addr}")
    # openvswitch bridge create and info
    quiet_exec(f"ovs-vsctl add-br br{br_id}")
    quiet_exec(f"ovs-vsctl set bridge br{br_id} protocols=OpenFlow13")
    # ovs-appctl bridge/dump-flows br0
    quiet_exec(f"ovs-vsctl set-controller br{br_id} tcp:{openflow_addr}")
    quiet_exec(
        f"ovs-vsctl -- --id=@sflow create sflow agent=br{br_id} target=\"{sflow_addr}\" sampling=1000 polling=5 -- set bridge br{br_id} sflow=@sflow")
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
        # prepare string
        line = str(line).replace("\\n'", "").strip()
        cmd_split_first = line.split(": renamed from ")
        eth_num = cmd_split_first[1]
        cmd_split_second = cmd_split_first[0].split(" ")
        ens_num = cmd_split_second[-1]

        # for virtualbox needs
        if line.__contains__("e1000"):
            pci_addr = line.split("e1000 ")[1].split(" " + ens_num)[0]
            interface_names.append({"old": eth_num, "new": ens_num, "pci_addr": pci_addr})
        # for openstack
        else:
            iface_id = ens_num.replace("ens", "")
            interface_names.append({"old": eth_num, "new": ens_num, "pci_addr": f"0000:00:0{iface_id}.0"})
    return interface_names


def dpdk_conf(pci_addr, br_id, ip_end):
    run('sysctl -w vm.nr_hugepages=1024')
    if 'nr_hugepages' not in open('/etc/sysctl.conf').read():
        run('echo "vm.nr_hugepages=1024" >> /etc/sysctl.conf')
    run('echo "NR_2M_PAGES=256" > /etc/dpdk/dpdk.conf')
    run('echo "options vfio enable_unsafe_noiommu_mode=1" > /etc/modprobe.d/vfio-noiommu.conf')
    run(f"echo 'pci {pci_addr} vfio-pci' > /etc/dpdk/interfaces")
    # use openvswitch version with DPDK after reboot
    quiet_exec("update-alternatives --set ovs-vswitchd /usr/lib/openvswitch-switch-dpdk/ovs-vswitchd-dpdk")

    # add ip to bridge for vxlan connection
    quiet_exec("ovs-vsctl --no-wait set Open_vSwitch . other_config:dpdk-init=true")
    quiet_exec(
        f"ovs-vsctl add-br br{br_id} -- set bridge br{br_id} datapath_type=netdev -- set bridge br{br_id} fail-mode=standalone"
    )
    quiet_exec(
        f"ovs-vsctl add-port br{br_id} dpdk-p1 -- set Interface dpdk-p1 type=dpdk options:dpdk-devargs={pci_addr}"
    )

    # detect VM name to set other IP and prevent network conflict
    hostname = socket.gethostname()
    if hostname == "vm2":
        ip_end_next = int(ip_end) + 1
        quiet_exec(f"ip addr add 172.16.0.{ip_end_next}/24 dev br{br_id}")
    else:
        quiet_exec(f"ip addr add 172.16.0.{ip_end}/24 dev br{br_id}")

    # bridge all set, wake up already!
    quiet_exec(f"ip link set br{br_id} up")


def autostart():
    final_path = "/opt/frackmic/network-task/"
    this_file_path = os.path.abspath(__file__)
    this_folder_path = Path().absolute()
    # make dir for safe install
    quiet_exec(f"mkdir -p {final_path}")
    quiet_exec(f"cp {this_folder_path}/*.ini {this_folder_path}/*.py {final_path}")
    run(
        f'echo "[Unit]\nDescription = network fun\nRequires=systemd-networkd.service\n\n[Service]\nType=oneshot\nWorkingDirectory={final_path}\nExecStart=/usr/bin/python3 {final_path}network.py\n\n[Install]\nWantedBy=network-online.target" > /etc/systemd/system/lab.service '
    )
    quiet_exec("systemctl enable lab.service")
    log("Added to start @ boot")

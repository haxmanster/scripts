### 3MVS
---
# -*- mode ruby -*-
# vi: set ft=ruby :

servers=[
  {
    :hostname => "Vm1",
    :ip => "192.168.100.10",
    :box => "ubuntu/bionic64",
    :ram => "6144",
    :cpu => "4",
    :file => "ubuntu.sh"
    :no_proxy => "192."
    :proxy => "domain:port"
  },
  {
    :hostname => "Vm2",
    :ip => "192.168.100.11",
    :box => "ubuntu/bionic64",
    :ram => "9600",
    :cpu => "6",
    :file => "ubuntu.sh"
    :no_proxy => "192."
    :proxy => "domain:port"
   },
   {
    :hostname => "Vm3",
    :ip => "192.168.100.12",
    :box => "centos/7",
    :ram => "12800",
    :cpu => "8",
    :file => "centos.sh"
    :no_proxy => "192."
    :proxy => "domain:port"
   }
]

Vagrant.configure("2") do |config|
    servers.each do |machine|
        config.vm.define machine[:hostname] do |node|
           node.vm.box = machine[:box]
           node.vm.hostname = machine[:hostname]
           node.vm.network "private_network", ip: machine[:ip]
           node.proxy.http = machine[:proxy]
           node.proxy.no_proxy = machine[:no_proxy]
           node.vm.provision "file", source: "~/.ssh/id_rsa.pub", destination: "id_rsa.pub"
           node.vm.provision "shell", inline: "cat id_rsa.pub >> /home/vagrant/.ssh/authorized_keys"
           node.vm.provision "shell", path: machine[:file]
           node.vm.provider "virtualbox" do |vb|
             vb.customize ["modifyvm", :id, "--memory" , machine[:ram], "--cpus", machine[:cpu]]
           end
        end
    end
end
```

```
# -*- mode ruby -*-
# vi: set ft=ruby :

servers=[
  {
    :hostname => "phoronix",
    :ip => "192.177.100.10",
    :box => "ubuntu/bionic64",
    :ram => "6144",
    :cpu => "4",
    :file => "ubuntu.sh"
  },
  {
    :hostname => "phoronix1",
    :ip => "192.177.100.11",
    :box => "ubuntu/bionic64",
    :ram => "9600",
    :cpu => "6",
    :file => "ubuntu.sh"
   },
   {
    :hostname => "phoronix2",
    :ip => "192.177.100.12",
    :box => "centos/7",
    :ram => "12800",
    :cpu => "8",
    :file => "centos.sh"
   }
]

Vagrant.configure("2") do |config|
    servers.each do |machine|
        config.vm.define machine[:hostname] do |node|
           node.vm.box = machine[:box]
           node.vm.hostname = machine[:hostname]
           node.vm.network "private_network", ip: machine[:ip]
           node.proxy.http = "http://proxy-us.intel.com:911"
           node.proxy.no_proxy = "localhost,127.0.0.1,192.177.40.10,192.177.40.11,192.177.40.12"
           node.vm.provision "shell", path: machine[:file]
           node.vm.provider "virtualbox" do |vb|
             vb.customize ["modifyvm", :id, "--memory" , machine[:ram], "--cpus", machine[:cpu]]
           end
        end
    end
end
```

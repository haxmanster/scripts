# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.define "VM1" do |vm1|
    vm1.vm.box = "ubuntu/bionic64"
    vm1.vm.hostname = "vm1"
    vm1.vm.network "private_network", ip: "10.20.30.1", auto_config: false
  end
  
  config.vm.define "VM2" do |vm2|
    vm2.vm.box = "ubuntu/bionic64"
    vm2.vm.hostname = "vm2"
    vm2.vm.network "private_network", ip: "10.20.30.2", auto_config: false
  end
  
  config.vm.provider "virtualbox" do |vb|
    vb.memory = "4096"
  end

  config.vm.provision "shell", inline: <<-SHELL
    cd /vagrant && python3 network.py
  SHELL
end

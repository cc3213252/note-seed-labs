# -*- mode: ruby -*-
# vi: set ft=ruby :

hosts = [{
   hostname: "seedlab",
   ip: "192.168.0.11",
   memory: "2048",
   cpus: 1,
}]


Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-20.04"
  config.ssh.insert_key = true
  config.hostmanager.enabled = true
  config.hostmanager.manage_host = true
  config.vm.box_check_update = false

  hosts.each_with_index do |host, index|
    config.vm.define host[:hostname] do |node|
      node.vm.hostname = host[:hostname]
      node.vm.network "private_network", ip: host[:ip]
      node.vm.provider "virtualbox" do |vb|
        vb.memory = host[:memory]
        vb.cpus = host[:cpus]
      end
    end
  end
end


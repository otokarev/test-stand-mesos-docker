# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "centos/7"
  config.vm.synced_folder ".", "/home/vagrant/sync", disabled: true

  config.vm.provision "shell" do |s|
    ssh_pub_key = File.readlines("#{Dir.home}/.ssh/id_rsa.pub").first.strip
    s.inline = <<-SHELL
      echo #{ssh_pub_key} >> /home/vagrant/.ssh/authorized_keys
      chmod 600 /home/vagrant/.ssh/authorized_keys
    SHELL
  end

    (2..3).each do |i|
      config.vm.define "master#{i}" do |c|
        c.vm.provider "virtualbox" do |v|
          v.cpus = 4
          v.memory = 1600
        end
        c.vm.network "private_network", ip: "192.168.2.#{i}"
        c.vm.hostname = "master#{i}.mesos.boom"
      end
    end

    (5..7).each do |i|
      config.vm.define "slave#{i}" do |c|
        c.vm.provider "virtualbox" do |v|
          v.memory = 2048
          v.cpus = 2
        end
        c.vm.network "private_network", ip: "192.168.2.#{i}"
        c.vm.hostname = "slave#{i}.mesos.boom"
      end
    end

end

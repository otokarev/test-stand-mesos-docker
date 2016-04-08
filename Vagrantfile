# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "centos/7"

  config.vm.provision "shell" do |s|
    ssh_pub_key = File.readlines("#{Dir.home}/.ssh/id_rsa.pub").first.strip
    s.inline = <<-SHELL
      echo #{ssh_pub_key} >> /home/vagrant/.ssh/authorized_keys
      chmod 600 /home/vagrant/.ssh/authorized_keys
    SHELL
  end

#  config.vm.define "docker-registry1" do |c|
#    c.vm.network "private_network", ip: "192.168.2.4"
#    c.vm.hostname = "hui.boom"
#    c.vm.provision "ansible" do |a|
#      a.limit = "docker-registry1"
#      a.playbook = "playbooks/docker-registry/playbook.yml"
#      a.raw_arguments = [
#        '-K'
#      ]
#    end
#  end

#    (2..4).each do |i|
#      config.vm.define "master#{i}" do |c|
#        c.vm.provider "virtualbox" do |v|
#          v.cpus = 4
#          v.memory = 2048
#        end
#        c.vm.network "private_network", ip: "192.168.2.#{i}"
#        c.vm.hostname = "master#{i}.mesos.boom"
##        c.vm.provision "ansible" do |a|
##          a.limit = "all"
##          a.playbook = "playbooks/mesos-single/playbook.yml"
##          a.groups = {
##            "mesos-single" => ["master#{i}"]
##          }
##          a.extra_vars = {
##            domain_name: "master#{i}.mesos.boom",
##            host_ip: "192.168.2.#{i}",
##            zoo_myid: "#{i}"  
##            }
##        end
#      end
#    end
#
#    (5..7).each do |i|
#      config.vm.define "slave#{i}" do |c|
#        c.vm.provider "virtualbox" do |v|
#          v.memory = 2048
#          v.cpus = 2
#        end
#        c.vm.network "private_network", ip: "192.168.2.#{i}"
#        c.vm.hostname = "slave#{i}.mesos.boom"
##        c.vm.provision "ansible" do |a|
##          a.limit = "all"
##          a.playbook = "playbooks/mesos-single/playbook.yml"
##          a.groups = {
##            "mesos-slave" => ["slave#{i}"]
##          }
##          a.extra_vars = {
##            domain_name: "slave#{i}.mesos.boom",
##            host_ip: "192.168.2.#{i}",
##            }
##        end
#      end
#    end

    #
    # Docker registry
    #
    config.vm.define "docker-hub" do |c|
      c.vm.provider "virtualbox" do |v|
        v.memory = 512
        v.cpus = 1
      end
      c.vm.network "private_network", ip: "192.168.2.8"
      c.vm.hostname = "docker-hub-test.openprovider.nl"
    end
end

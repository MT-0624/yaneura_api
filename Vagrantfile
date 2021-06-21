# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
    config.vm.define "yaneura-machine"

    config.vm.box = "ubuntu/focal64"
    config.vm.hostname = "yaneura-machine"

    # Disable automatic box update checking. If you disable this, then
    # boxes will only be checked for updates when the user runs
    # `vagrant box outdated`. This is not recommended.
    config.vm.box_check_update = true
    config.vm.network "forwarded_port", guest: 8080, host: 8080
    config.vm.network "forwarded_port", guest: 3306, host: 13306

    config.vm.synced_folder "./", "/vagrant"

    config.vm.provision "ansible_local" do |ansible|
      ansible.playbook = "/vagrant/playbook/playbook.yml"
    end
end

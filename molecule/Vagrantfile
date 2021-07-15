
Vagrant.configure("2") do |config|
  config.vm.hostname = "mastodon"
  config.vm.box = "generic/ubuntu2004"
  config.ssh.keys_only = false

  config.vm.synced_folder "./", "/vagrant", type: "rsync"

  config.vm.provider "libvirt"
  config.vm.provider :libvirt do |libvirt|
    libvirt.title = "mastodon"
  end
end


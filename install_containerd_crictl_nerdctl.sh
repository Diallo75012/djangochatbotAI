#!/usr/bin/bash

# this files installs containerd crictl to run it like docker and nerdctl to have support for docker-compose files
set -e  # Exit immediately if a command fails
set -o pipefail  # Catch errors in piped commands


# Install containerd
sudo apt update
sudo apt install -y containerd

# Configure containerd
sudo mkdir -p /etc/containerd
sudo containerd config default | sudo tee /etc/containerd/config.toml
# Restart containerd
sudo systemctl restart containerd
sudo systemctl enable containerd

# OR install ROOTLESS containerd , but has some limitation for prod. port 80 not supported, networking issue, postgresql..etc.. so not for now
# sudo apt install -y uidmap dbus-user-session
# curl -fsSL https://get.rootlesscontaine.rs | bash
# rootlesskit --version
# containerd-rootless-setuptool.sh install
# containerd-rootless-setuptool.sh check

# Install crictl
VERSION="v1.32.0"  # Check latest version at https://github.com/kubernetes-sigs/cri-tools/releases
wget https://github.com/kubernetes-sigs/cri-tools/releases/download/${VERSION}/crictl-${VERSION}-linux-amd64.tar.gz
sudo tar -C /usr/local/bin -xzf crictl-${VERSION}-linux-amd64.tar.gz
rm crictl-${VERSION}-linux-amd64.tar.gz

# Install nerdctl and buildkitd for it work. so we need a service called `buildkitd` to run to be able to build images
VERSION="1.7.3"  # Check latest version at https://github.com/containerd/nerdctl/releases
wget https://github.com/containerd/nerdctl/releases/download/v${VERSION}/nerdctl-${VERSION}-linux-amd64.tar.gz
sudo tar -C /usr/local/bin -xzf nerdctl-${VERSION}-linux-amd64.tar.gz
rm nerdctl-${VERSION}-linux-amd64.tar.gz
echo "🔹 Finding the latest BuildKit release..."
BUILDKIT_URL=$(curl -s https://api.github.com/repos/moby/buildkit/releases/latest | grep browser_download_url | grep linux-amd64.tar.gz | cut -d '"' -f 4)
if [[ -z "$BUILDKIT_URL" ]]; then
  echo "❌ Failed to fetch the latest BuildKit release URL."
  exit 1
fi
echo "✅ Latest BuildKit release found: $BUILDKIT_URL"
# Download the BuildKit archive
echo "🔹 Downloading BuildKit..."
wget -O buildkit.tar.gz "$BUILDKIT_URL"
# Extract BuildKit binaries
echo "🔹 Extracting BuildKit..."
sudo tar -xvf buildkit.tar.gz -C /usr/local
# Move binaries to /usr/bin/ for system-wide access
echo "🔹 Moving BuildKit binaries to /usr/bin/..."
sudo mv /usr/local/bin/buildctl /usr/bin/
sudo mv /usr/local/bin/buildkitd /usr/bin/
# Cleanup
rm buildkit.tar.gz
# Check if systemd service exists
SERVICE_PATH="/etc/systemd/system/buildkit.service"
if [ ! -f "$SERVICE_PATH" ]; then
    echo "🔹 Creating systemd service for BuildKit..."
    sudo bash -c "cat > $SERVICE_PATH" <<EOF
[Unit]
Description=BuildKit Daemon
After=network.target

[Service]
ExecStart=/usr/bin/buildkitd
Restart=always
User=root
Group=root

[Install]
WantedBy=multi-user.target
EOF

    echo "✅ Systemd service created."
else
    echo "✅ Systemd service already exists."
fi
# Reload systemd, enable, and start the service
echo "🔹 Enabling and starting BuildKit service..."
sudo systemctl daemon-reload
sudo systemctl enable --now buildkit
# Check service status
echo "🔹 Checking BuildKit service status..."
sudo systemctl status buildkit --no-pager

# install networking CNI plugin to be able to run container images
CNI_PLUGINS_VERSION="v1.3.0"  # Adjust to the latest version
CNI_INSTALL_DIR="/opt/cni/bin"

echo "🔹 Checking if CNI plugins are already installed..."
if [ -d "$CNI_INSTALL_DIR" ] && [ -n "$(ls -A $CNI_INSTALL_DIR 2>/dev/null)" ]; then
    echo "✅ CNI plugins already installed in $CNI_INSTALL_DIR"
    exit 0
fi
echo "🔹 Installing CNI plugins..."
mkdir -p "$CNI_INSTALL_DIR"
curl -L -o /tmp/cni-plugins.tgz "https://github.com/containernetworking/plugins/releases/download/$CNI_PLUGINS_VERSION/cni-plugins-linux-amd64-$CNI_PLUGINS_VERSION.tgz"
echo "🔹 Extracting plugins to $CNI_INSTALL_DIR..."
tar -xvzf /tmp/cni-plugins.tgz -C "$CNI_INSTALL_DIR"
echo "🔹 Setting correct permissions..."
chmod +x "$CNI_INSTALL_DIR"/*
echo "✅ CNI plugins installed successfully!"

# Add alias only if it is not already in ~/.bashrc
if ! grep -q "alias docker='nerdctl'" ~/.bashrc; then
  echo "alias docker='nerdctl'" >> ~/.bashrc
fi
if ! grep -q "alias docker-compose='nerdctl compose'" ~/.bashrc; then
  echo "alias docker-compose='nerdctl compose'" >> ~/.bashrc
fi
# Reload ~/.bashrc to apply changes
source ~/.bashrc

# Test installation
crictl --version
containerd --version
nerdctl --version
# Verify installation
echo "✅ BuildKit installation completed!"
echo "🔹 Verifying installation..."
buildctl --version
buildkitd --version


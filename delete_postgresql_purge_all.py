sudo systemctl stop postgresql
sudo DEBIAN_FRONTEND=noninteractive apt remove --purge postgresql postgresql-* -y
sudo rm -rf /etc/postgresql /var/lib/postgresql
sudo deluser postgres
sudo delgroup postgres
sudo rm -rf /etc/apt/sources.list.d/pgdg.list
sudo rm -rf /etc/apt/keyrings/postgresql.asc
sudo apt autoremove -y
sudo apt autoclean
dpkg -l | grep postgresql
# optional
#sudo reboot

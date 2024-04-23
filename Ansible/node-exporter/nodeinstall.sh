#!/bin/bash

cd ~/

wget https://github.com/prometheus/node_exporter/releases/download/v1.7.0/node_exporter-1.7.0.linux-amd64.tar.gz
tar -xzvf node_exporter-1.7.0.linux-amd64.tar.gz 

sudo useradd -m node_exporter
sudo groupadd node_exporter
sudo usermod -a -G node_exporter node_exporter

cp node_exporter-1.7.0.linux-amd64/* /usr/local/bin
sudo chown node_exporter:node_exporter /usr/local/bin/node_exporter

cat <<EOF > /etc/systemd/system/node_exporter.service
[Unit]
Description=Node Exporter
After=network.target

[Service]
User=node_exporter
Group=node_exporter
Type=simple
ExecStart=/usr/local/bin/node_exporter

[Install]
WantedBy=multi-user.target
EOF

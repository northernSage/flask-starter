#!/bin/bash

export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get -y upgrade

# extra required packages can be installed here

apt-get clean
rm -rf /var/lib/apt/lists/*
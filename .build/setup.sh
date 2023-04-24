#!/bin/bash

#############################################################
#  usage: ./setup.sh

#### EXAMPLES
## Install deps for first time setup on a device (so that the project Makefile runs!)
# $ ./setup.sh
#############################################################

export NAME="[setup.sh]: "
echo "${NAME} STARTING "

# Bash failure reporting for the script
set -eE -o functrace
failure() {
  local lineno=$1
  local msg=$2
  echo "${NAME} Failed at $lineno: $msg"
}
trap '${NAME} failure ${LINENO} "$BASH_COMMAND"' ERR

#############################################################

echo "${NAME} Installing apt packages "
sudo apt-get update -y -qq &&
  sudo apt-get install $(cat project.apt)

echo "${NAME} starting docker installation steps, visit link for debugging and more info: https://get.docker.com/"
cd ~; curl -fsSL https://get.docker.com -o get-docker.sh
cd ~; sh get-docker.sh
cd ~; rm -rf get-docker.sh

echo "${NAME} docker post-installation: adding user to the docker group"
sudo usermod -aG docker "${USER}"
newgrp docker
sudo mkdir /home/"$USER"/.docker
sudo chown "$USER":"$USER" /home/"$USER"/.docker -R
sudo chmod g+rwx "$HOME/.docker" -R
docker run hello-world

echo "${NAME} FINISHED"
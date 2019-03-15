#!/bin/bash

# Steps to make this installation work:
#######################################
# Create directory ~/local
# Navigate to that directory
# Figure out if curl or wget is installed, then
# 	download source files for python3, stripe, and flask
#	unzip the file archives
#	navigate into the directory that contains the  build file
#	run installation scripts for each package
#	delete the archives if they exist

mkdir -p ~/SeedFoundryApp
mkdir -p ~/SeedFoundryApp/local
cd ~/SeedFoundryApp/local

if [[ -a "$(command -v curl)" ]]; then
	curl -v https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tgz
elif [[ -a "$(command -v wget)" ]]; then
	wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tgz
else 
	echo "Please install either curl or wget to proceed with installation"
fi

if [[ -a "$)command -v tar)" ]]; then
	tar -zxvf Python-3.7.2.tgz
elif [[ -a "$)command -v unzip)" ]]; then
	unzip Python-3.7.2.tgz -d ~/local
fi

cd Python-3.7.2
./configure --enable-optimizations --with-ensurepip=install
make -j 8
make test
make install

pip install stripe
pip install flask

echo "Installation successful. Please paste your PUBLISHABLE key from Stripe dashboard and press ENTER:"
read publishable_key
echo "Now please paste your SECRET key from Stripe dashboard and press ENTER:"
read secret_key
export PUBLISHABLE_KEY="$publishable_key"
export SECRET_KEY="$secret_key"

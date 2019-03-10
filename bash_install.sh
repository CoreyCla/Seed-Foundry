#!/bin/bash

# Steps to make this installation work:
#######################################
# Create directory ~/local
# Navigate to that directory
# Figure out if curlor wget is installed, then
# 	download source files for python3, stripe, and flask
#	unzip the file archives
#	navigate into the directory that contains the  build file
#	run installation scripts for each package
#	delete the archives if they exist

mkdir -p ~/local
cd ~/local

if [ -x "$(command -v curl)" ]; then
	curl https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tgz
elif [ -x "$(command -v wget)" ]; then
	wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tgz
else 
	echo "Please install either curl or wget to proceed with installation"

if [ -x "$)command -v tar)" ]; then
	tar -zxvf Python-3.7.2.tgz
elif [ -x "$)command -v unzip)" ]; then
	unzip Python-3.7.2.tgz -d ~/local

cd Python-3.7.2
./configure --enable-optimizations --with-ensurepip=install
make -j 8
make altinstall

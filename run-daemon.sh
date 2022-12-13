#!/bin/bash

sudo apt-get install -y python3-pip

pip3 install schedule

python3 kaveh-daemon.py $1

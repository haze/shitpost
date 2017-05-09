#!/bin/sh
pip3 install Nuitka
nuitka --show-progress --lto --remove-output src/shitpost.py
sudo mv shitpost.exe /usr/local/bin/shitpost
echo 'done'
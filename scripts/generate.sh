#!/bin/sh
cd $(dirname "$0")
cd ..

rm -rf imgs
mkdir imgs

coin.py plot -d 1 -g 1 -m l -o imgs/coin-length.png
coin.py plot -d 1 -g 10 -m w -o imgs/coin-width.png

coin_phy.py plot -d 1 -g 1 -m l -o imgs/coin-phy-length.png
coin_phy.py plot -d 1 -g 10 -m w -o imgs/coin-phy-width.png

needle.py plot -l 1 -g 1 -m l -o imgs/needle-length.png
needle.py plot -l 1 -g 10 -m w -o imgs/needle-width.png

needle_phy.py plot -l 1 -g 1 -m l -o imgs/needle-phy-length.png
needle_phy.py plot -l 1 -g 10 -m w -o imgs/needle-phy-width.png

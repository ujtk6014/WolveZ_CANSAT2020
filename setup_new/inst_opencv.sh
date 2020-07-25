#!/bin/bash
#Opencv&Numpyのインストールファイル
#Last update 2020/07/08 Yuji Tanaka

#必要なモジュールのインストール
sudo apt-get install libhdf5-dev libhdf5-serial-dev libhdf5-103
sudo apt-get install libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5
sudo apt-get install libatlas-base-dev
sudo apt-get install libjasper-dev

#Opencvnoインストール（あえてバージョンを落としてバグらないようにする）
sudo pip3 --default-timeout=1000 install opencv-python==4.1.0.25
sudo pip3 install opencv-contrib-python==4.1.0.25

#なんかわかんないけど必要な作業
LD_PRELOAD=/usr/lib/arm-linux-gnueabihf/libatomic.so.1
sudo echo "export LD_PRELOAD=/usr/lib/arm-linux-gnueabihf/libatomic.so.1">>~/.bashrc

#!/bin/bash
#GPSのセットアップ
#Last update 2020/07/08 Yuji Tanaka
#<<実行方法>>
#bash setup_gps.sh
#./setup_gps.sh
#上記２つのどちらかのコマンドをターミナルに打ち込む

#/boot/cmdline.txtの修正
sudo cat /boot/cmdline.txt|tr -d console=serial0,115200
sudo cat /boot/cmdline.txt

#Serial Mosuleのインストール
sudo apt-get install python-serial

#実行権限を与える
sudo chmod +x setup_gps.sh

#設定完了の喜びの舞
echo -e "<<設定完了のおしらせ>>\nおめでとう！設定完了だ！君はまだ強くなれる。"
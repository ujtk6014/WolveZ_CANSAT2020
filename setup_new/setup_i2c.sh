#!/bin/bash
#i2c通信のセットアップ
#last update 2020/07/08 Yuji Tanaka
#<<実行方法>>
#bash setup_i2c.sh
#./setup_i2c.sh
#上記２つのどちらかのコマンドをターミナルに打ち込む

#moduleファイルに以下の項目を追加
sudo echo "i2c-bcm2708\ni2c-dev">>/etc/modules


#update
sudo apt-get update

#i2cのtoolをインストール
sudo apt-get install -y python-smbus i2c-tools

#設定完了の喜びの舞
echo -e "<<設定完了のおしらせ>>\nおめでとう！設定完了だ！ともに高みへゆこう\n10秒後にラズパイを再起動します。"

#reboot after 10s
sudo shutdown -r +10


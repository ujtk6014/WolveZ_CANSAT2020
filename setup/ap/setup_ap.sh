#RPiのAP化初回セットアップ
#<<実行方法>>
#bash setup_ap.sh

#１．電通大さんの参考
sudo apt-get install hostapd
sudo apt install dnsmasq iptables

#create_apのインストール
git clone https://github.com/oblique/create_ap
cd create_ap
sudo make install
#create_ap.confの内容変更（他に楽な書き方絶対ありそう）
sudo sh -c "rm -rf /etc/create_ap.conf"
sudo sh -c "echo 'CHANNEL=default\nGATEWAY=10.0.0.1\nWPA_VERSION=2\nETC_HOSTS=0\nDHCP_DNS=gateway\nNO_DNS=0\nNO_DNSMASQ=0\nHIDDEN=0\nMAC_FILTER=0\nMAC_FILTER_ACCEPT=/etc/hostapd/hostapd.accept\nISOLATE_CLIENTS=0\nSHARE_METHOD=nat\nIEEE80211N=0\nIEEE80211AC=0\nHT_CAPAB=[HT40+]\nVHT_CAPAB=\nDRIVER=nl80211\nNO_VIRT=0\nCOUNTRY=\nFREQ_BAND=2.4\nNEW_MACADDR=\nDAEMONIZE=0\nNO_HAVEGED=0\nWIFI_IFACE=wlan0\nINTERNET_IFACE=lo\nSSID=wolvez2020\nPASSPHRASE=wolvez2020\nUSE_PSK=0'>>/etc/create_ap.conf"
#ssidとpassphraseは好きなもので
#echoだけだと'許可がありません'のエラーが発生した　参考→https://linuxfan.info/post-1818
#↓置換する方法（↑２つの書き方変えた版だけどうまく行ったり行かなかったり...保留）
#sudo sh -c "sed -i -- 's/GATEWAY=10.0.0.1/GATEWAY=10.1.1.3/g' /etc/create_ap.conf"
#sudo sh -c "sed -i -- 's/INTERNET_IFACE=eth0/INTERNET_IFACE=lo/g' /etc/create_ap.conf"
#sudo sh -c "sed -i -- 's/SSID=MyAccessPoint/SSID=wolvez2020/g' /etc/create_ap.conf"
#sudo sh -c "sed -i -- 's/PASSPHRASE=12345678/PASSPHRASE=wolvez2020/g' /etc/create_ap.conf"

sudo systemctl enable create_ap
sudo systemctl start create_ap


#２．１だけでAP化できなかったら（あとで確認）  （参考→http://norikyu.blogspot.com/p/raspberry-pi3-lan-ap.html）

#ファイル編集(network/interfaces, /etc/default/hostapd)
sudo sh -c "echo 'source-directory /etc/network/interfaces.d\nauto lo\niface lo inet loopback\niface eth0 inet manual\nauto wlan0\nallow-hotplug wlan0\niface wlan0 inet static\naddress 192.168.7.1\nnetmask 255.255.255.0'>>/etc/network/interfaces"
sudo sh -c 'echo "DAEMON_CONF="/etc/hostapd/hostapd.conf""'
#dnsmasqのインストール
sudo apt-get install dnsmasq
#オリジナル設定ファイルのバックアプ
sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig

#reboot 
echo -e "<<設定完了のおしらせ>>\nお疲れ様です！AP化初期設定完了！ 再起動お願いします！"
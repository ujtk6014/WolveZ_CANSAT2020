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

<<<<<<< HEAD
#ファイル編集(network/interfaces, /etc/default/hostapd)
sudo sh -c "echo 'source-directory /etc/network/interfaces.d\nauto lo\niface lo inet loopback\niface eth0 inet manual\nauto wlan0\nallow-hotplug wlan0\niface wlan0 inet static\naddress 192.168.7.1\nnetmask 255.255.255.0'>>/etc/network/interfaces"
sudo sh -c 'echo "DAEMON_CONF="/etc/hostapd/hostapd.conf""'
=======
#ファイル編集(network/interfaces, /etc/hostapd/hostapd.conf, /etc/default/hostapd)
#wlan0
#sudo sh -c "echo 'source-directory /etc/network/interfaces.d\nauto lo\niface lo inet loopback\niface eth0 inet manual\nauto wlan0\nallow-hotplug wlan0\niface wlan0 inet static\naddress 192.168.7.1\nnetmask 255.255.255.0'>>/etc/network/interfaces"
#hostapdのインストール
#sudo sh -c "echo 'interface=wlan0\ndriver=nl80211\nssid=wolvez2020\nhw_mode=g\nchannel=6\nieee80211n=1\nwmm_enabled=1\nht_capab=[HT40][SHORT-GI-20][DSSS_CCK-40]\nmacaddr_acl=0\nauth_algs=1\nignore_broadcast_ssid=0\nwpa=2\nwpa_key_mgmt=WPA-PSK\nwpa_passphrase=wolvez2020\nrsn_pairwise=CCMP'>>/etc/hostapd/hostapd.conf"
#sudo sh -c 'echo "DAEMON_CONF="/etc/hostapd/hostapd.conf""'

>>>>>>> 569eb148089b53f2eb81e67d2f5b9cdf92086246
#dnsmasqのインストール
#sudo apt-get install dnsmasq
#オリジナル設定ファイルのバックアプ
<<<<<<< HEAD
sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig

#reboot 
echo -e "<<設定完了のおしらせ>>\nお疲れ様です！AP化初期設定完了！ 再起動お願いします！"
=======
#sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
#ファイル編集(/etc/dnsmasq.conf)
#sudo sh -c "echo 'interface=wlan0\nlisten-address=192.168.7.1\nbind-interfaces\nserver=8.8.8.8\nserver=8.8.4.4\ndomain-needed\nbogus-priv\ndhcp-range=192.168.7.100,192.168.7.199,24h'>>/etc/dnsmasq.conf"

#reboot 
sudo reboot
>>>>>>> 569eb148089b53f2eb81e67d2f5b9cdf92086246

#AP化ON(２回目以降)　参考→http://norikyu.blogspot.com/p/raspberry-pi3-lan-ap.html
#<<実行方法>>
#bash sudo_ap_on.sh

#create_ap.confの内容変更
cd create_ap
sudo sh -c "rm -rf /etc/create_ap.conf"
sudo sh -c "echo 'CHANNEL=default\nGATEWAY=10.0.0.1\nWPA_VERSION=2\nETC_HOSTS=0\nDHCP_DNS=gateway\nNO_DNS=0\nNO_DNSMASQ=0\nHIDDEN=0\nMAC_FILTER=0\nMAC_FILTER_ACCEPT=/etc/hostapd/hostapd.accept\nISOLATE_CLIENTS=0\nSHARE_METHOD=nat\nIEEE80211N=0\nIEEE80211AC=0\nHT_CAPAB=[HT40+]\nVHT_CAPAB=\nDRIVER=nl80211\nNO_VIRT=0\nCOUNTRY=\nFREQ_BAND=2.4\nNEW_MACADDR=\nDAEMONIZE=0\nNO_HAVEGED=0\nWIFI_IFACE=wlan0\nINTERNET_IFACE=lo\nSSID=wolvez2020\nPASSPHRASE=wolvez2020\nUSE_PSK=0'>>/etc/create_ap.conf"

#sed -i -- 's/GATEWAY=10.0.0.1/GATEWAY=10.0.0.1/g' /etc/dnsmasq.conf
#sed -i -- 's/GATEWAY=10.0.0.1/WIFI_IFACE=wlan0/g' /etc/dnsmasq.conf
#sed -i -- 's/INTERNET_IFACE=eth0/INTERNET_IFACE=lo/g' /etc/dnsmasq.conf
#sed -i -- 's/SSID=MyAccessPoint/SSID=wolvez2020/g' /etc/dnsmasq.conf
#sed -i -- 's/PASSPHRASE=12345678/PASSPHRASE=wolvez2020/g' /etc/dnsmasq.conf
#ssidとpassphraseは好きなもの
#echoだけだと'許可がありません'のエラーが発生した　参考→https://linuxfan.info/post-1818

#↓のコメント外すとAP化されたRPiの無線だけが使用できるようになる
#AP化するために必要なファイル編集(2つ)
"""
cat > /etc/network/interfaces <<EOF

source-directory /etc/network/interfaces.d
auto lo
iface lo inet loopback
iface eth0 inet manual
auto wlan0
allow-hotplug wlan0
iface wlan0 inet static
address 192.168.7.1
netmask 255.255.255.0

EOF
"""
"""
cat > /etc/hostapd/hostapd.conf <<EOF

DAEMON_CONF=

EOF
"""


#enable, start
sudo systemctl enable create_ap
sudo systemctl start create_ap

sudo systemctl enable  hostapd
sudo systemctl start  hostapd

sudo systemctl enable  dnsmasq
sudo systemctl start  dnsmasq

#sudo reboot
echo -e "<<設定完了のおしらせ>>\nおめでとう！設定完了だ！ 再起動お願いします！"
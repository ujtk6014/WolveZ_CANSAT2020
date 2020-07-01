#GPSによる緯度経度（時間： , 緯度： , 経度：） 
#超音波センサによる距離（現在の距離：　）
#BNOによる加速度（x軸, y軸, z軸）
#の値が取れているかを確認するテスト

import gps
import ultrasonic
import BNO055_new
import time

TRIGPIN=23 #定数
ECHOPIN=18 #定数

try:
    GPS=gps.GPS()
    GPS.setupGPS()
    ultrasonic.setupUltrasonic(TRIGPIN,ECHOPIN)
    bno=BNO055_new.BNO055()
    if bno.begin() is not True:
        print("Error initializing device")
        exit()
    #time.sleep(1)
    bno.setExternalCrystalUse(True) 
    while True:
        GPS.gpsread()
        distance=ultrasonic.getDistance()
        print(bno.getVector(BNO055_new.BNO055.VECTOR_GYROSCOPE))
        #BNO055_new.testbno()
        time.sleep(1)

except KeyboardInterrupt:        #例外（CTRL+Cが押された時)処理
    ultrasonic_class.end()                       #endを実行



#GPSによる緯度経度（時間： , 緯度： , 経度：） 
#超音波センサによる距離（現在の距離：　）
#BNOによる加速度（x軸, y軸, z軸）
#の値が取れているかを確認するテスト

import gps
import ultrasonic
import bno055
import time
#import camera
#import cv2
import sys
import constant as ct
import RPi.GPIO as GPIO
import radio

class Test(object):
    
    def __init__(self):
        #オブジェクトの生成
        self.gps = gps.GPS()
        self.bno055 = bno055.BNO055()
        self.ultrasonic = ultrasonic.Ultrasonic()
        self.radio=radio.radio()
        #self.camera=camera.Camera()
        
    def setup(self):
        self.radio.setupRadio()
        self.gps.setupGps()
        if self.bno055.begin() is not True:
            print("Error initializing device")
            exit()
        
    
    def sensorWrite(self):
        self.gps.gpsread()
        self.bno055.bnoread()
        self.ultrasonic.getDistance()
        self.Ax=round(self.bno055.Ax,3)
        self.Ay=round(self.bno055.Ay,3)
        self.Az=round(self.bno055.Az,3)
        self.dist=round(self.ultrasonic.dist,2)
        
        datalog = str(self.gps.Time) + ","\
                  + str(self.gps.Lat) + ","\
                  + str(self.gps.Lon) + ","\
                  + str(self.bno055.gx) + ","\
                  + str(self.bno055.gy) + ","\
                  + str(self.bno055.gz) + ","\
                  + str(self.Ax) + ","\
                  + str(self.Ay) + ","\
                  + str(self.Az) + ","\
                  + str(self.dist)
        print(datalog)
    """
    def cam(self):
        #以下に画像処理走行プログラム
            _, frame = self.capture.read() # 動画の読み込み
            # frame=cv2.resize(frame, (640,480)) # プレビューサイズ（いじらなくてよい）
            rects = self.camera.find_rect_of_target_color(frame) # 矩形の情報作成
            
            if len(rects) > 0:
                rect = max(rects, key=(lambda x: x[2] * x[3]))  # 最大の矩形を探索
                
                #各パラメータの計算
                self.camera.find_center_of_gravity(rect) # 重心の計算
           
                cv2.rectangle(frame, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), (0, 0, 255), thickness=2) # フレームを生成
            cv2.drawMarker(frame,(self.camera.cgx,self.camera.cgy),(60,0,0))
            cv2.imshow('red', frame)
            cv2.waitKey(1)
    """        
    def sendRadio(self):
        datalog = str(self.gps.Lat) + ","\
                  + str(self.gps.Lon) + ","\
                  + str(self.bno055.gx) + ","\
                  + str(self.bno055.gy) + ","\
                  + str(self.bno055.gz) + ","\
                  + str(self.Ax) + ","\
                  + str(self.Ay) + ","\
                  + str(self.Az) + ","\
                  + str(self.dist)
        self.radio.sendData(datalog) #データを送信

if __name__ == "__main__":
    test=Test()
    test.setup()
    #test.capture = cv2.VideoCapture(0)
    try:
        while True:
            test.sensorWrite()
            test.sendRadio()
            time.sleep(1)
            #test.cam()
            #time.sleep(0.01)
    except KeyboardInterrupt:
        print('finished')
        GPIO.cleanup()
        pass


   




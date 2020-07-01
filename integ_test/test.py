#GPSによる緯度経度（時間： , 緯度： , 経度：） 
#超音波センサによる距離（現在の距離：　）
#BNOによる加速度（x軸, y軸, z軸）
#の値が取れているかを確認するテスト

import gps
import ultrasonic
import bno055
import time
import camera
import cv2
import sys
import constant as ct


class Test(object):
    
    def __init__(self):
        #オブジェクトの生成
        self.gps = gps.GPS()
        self.bno055 = bno055.BNO()
        self.radio = radio.radio()
        ultrasonic.setupUltrasonic(ct.const.ULTRASONIC_TRIG,ct.const.ULTRASONIC_ECHO)
        self.camera=camera.Camera()
        
    def setup(self):
        self.gps.setupGps()
        if self.bno.begin() is not True:
            print("Error initializing device")
            exit()
        self.bno.setExternalCrystalUse(True)
        
        
    
    def sensorWrite(self):
        self.gps.gpsread()
        self.bno055.bnoread()
        ultrasonic.getDistance()
        datalog = str(self.timer) + ","\
                  + str(self.gps.Time) + ","\
                  + str(self.gps.Lat) + ","\
                  + str(self.gps.Lon) + ","\
                  + str(self.bno055.gx) + ","\
                  + str(self.bno055.gy) + ","\
                  + str(self.bno055.gz) + ","\
                  + str(self.bno055.Ax) + ","\
                  + str(self.bno055.Ay) + ","\
                  + str(self.bno055.Az) + ","\
                  + str(self.ultrasonic.distance)
        print(datalog)
    
    def camera(self):
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

if __name__ == "__main__":
    test=Test()
    test.setup()
    self.capture = cv2.VideoCapture(0)
    try:
        while True:
            test.sensorWrite()
            sleep(0.01)
            test.camera()
            sleep(0.01)
    except KeyboardInterrupt:
        print('finished')
        GPIO.cleanup()
        pass


   




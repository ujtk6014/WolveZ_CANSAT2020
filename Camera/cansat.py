import cv2
#import numpy as np
import sys

import constant as ct
import motor
import camera
import ultrasonic
import bno055

class Cansat(object):
    
    def __init__(self):
        self.countAreaLoopEnd=0 # 終了判定用
        self.countAreaLoopStart=0 # 開始判定用
        self.countAreaLoopLose=0 # 見失い判定用
        self.countDistanceLoopStart=0
        self.countDistanceLoopEnd=0
        
        self.state=1
        self.following=0 # state1の中で、カメラによる検知中か追従中かを区別、どちらもカメラを回しながら行いたいため
        
        self.camera=camera.Camera()
        self.ultrasonic=ultrasonic.Ultrasonic()
        self.bno055=bno055.BNO055()#クラス名のみ変えたため注意
        self.rightmotor = motor.motor(ct.const.RIGHT_MOTOR_IN1_PIN,ct.const.RIGHT_MOTOR_IN2_PIN,ct.const.RIGHT_MOTOR_VREF_PIN)
        self.leftmotor = motor.motor(ct.const.LEFT_MOTOR_IN1_PIN,ct.const.LEFT_MOTOR_IN2_PIN,ct.const.LEFT_MOTOR_VREF_PIN)
        
        self.timestep=0

    def sequence(self):
        if self.state==0:
            self.waiting()
        elif self.state==1:
            self.running()
        elif self.state==2:
            self.finish()
        else:
            self.state=0
    
    def setup(self):
        self.bno055.setupBno(True)
        #self.camera.setupCamera()#ガンマ補正のためのセットアップ

    def sensor(self):
        self.bno055.bnoread()
        datalog= str(self.rightmotor.velocity).rjust(6) + ","\
               + str(self.leftmotor.velocity).rjust(6)
        print(datalog)
        #print('Ax=',self.bno055.Ax,',Ay=',self.bno055.Ay,',Az=',self.bno055.Az)
        #print('gx=',self.bno055.gx,',gy=',self.bno055.gy,',gz=',self.bno055.gz)

    def waiting(self):
        self.ultrasonic.getDistance()
        #print(self.ultrasonic.dist)
        if self.ultrasonic.dist<ct.const.DISTANCE_THRE_START:
            self.countDistanceLoopStart+=1
            if self.countDistanceLoopStart>ct.const.COUNT_DISTANCE_LOOP_THRE_START:
                print("対象認知＆カメラ処理開始")
                self.state=1
                self.countDistanceLoopStart=0
        else:
            self.countDistanceLoopStart=0


    def running(self):
        #写真撮影用
        self.timestep+=1
        #print(self.ultrasonic.dist)
        _, frame = self.capture.read() # 動画の読み込み
        # frame=cv2.resize(frame, (640,480)) # プレビューサイズ（いじらなくてよい）
        
        """
        #以下でガンマ補正
        gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        mean, stddev=cv2.meanStdDev(gray)
        if stddev>ct.const.BLACKLIGHT_SD_UP or stddev<ct.const.BLACKLIGHT_SD_DOWN:
            frame=cv2.LUT(frame,self.camera.gamma_cvt)
        """
        
        # 矩形の情報作成
        rects = self.camera.find_rect_of_target_color(frame) 
        
        """
        # 一定間隔で状況を撮影
        if self.timestep%200==0:
            imName=str(self.timestep)+'image.jpg'
            cv2.imwrite(imName,frame)
        """
        
        if len(rects) > 0:
            rect = max(rects, key=(lambda x: x[2] * x[3]))  # 最大の矩形を探索
            
            #各パラメータの計算
            self.camera.find_center_of_gravity(rect) # 重心の計算
            self.camera.find_angle(self.camera.cgx) # 角度の計算、絶対値
            self.camera.find_direction(self.camera.cgx) # 進む方向
            self.camera.find_area(rect) # 矩形の面積算出
            
            #追従開始判定
            if self.following==0 and self.camera.area>ct.const.AREA_THRE_START:
                self.countAreaLoopStart+=1
                if self.countAreaLoopStart==1:
                    self.camera.cgxs=self.camera.cgx
                    self.camera.cgys=self.camera.cgy
                if self.countAreaLoopStart>ct.const.COUNT_AREA_LOOP_THRE_START:
                    if pow(self.camera.cgx-self.camera.cgxs,2)+pow(self.camera.cgy-self.camera.cgys,2)>ct.const.COG_THRE_START:
                        print("追従開始")
                        self.following=1
                        self.countAreaLoopStart=0
            else:
                self.countAreaLoopStart=0
            
            #モーターへの指示を行う
            if self.following==1:
                #print('モーターへの指示')
                if self.camera.direct==0:
                        self.rightmotor.go(100)
                        self.leftmotor.go(100)
                
                if self.camera.direct==1:
                        self.rightmotor.go(100)
                        self.leftmotor.go(round(100*(1-self.camera.angle/ct.const.MAX_CAMERA_ANGLE)))
                        
                if self.camera.direct==-1:
                        self.rightmotor.go(round(100*(1-self.camera.angle/ct.const.MAX_CAMERA_ANGLE)))
                        self.leftmotor.go(100)
            
            """
            #見失い判定
            if self.following==1 and self.camera.area<ct.const.AREA_THRE_LOSE:
                self.countAreaLoopLose+=1
                if self.countAreaLoopLose>ct.const.COUNT_AREA_LOOP_THRE_LOSE:
                    self.state=0
                    self.countAreaLoopLose=0
                    self.following=0
                    print('見失った！')
                    cv2.destroyAllWindows()
            else:
                self.countAreaLoopLose=0
            """
            
            """
            #超音波センサを用いた終了判定
            self.ultrasonic.getDistance()
            if self.following==1 and self.ultrasonic.dist<ct.const.DISTANCE_THRE_END:
                self.countDistanceLoopEnd+=1
                if self.countDistanceLoopEnd>ct.const.COUNT_DISTANCE_LOOP_THRE_END:
                    print("追従終了")
                    self.state=2
            else:
                self.countDistanceLoopEnd=0
            """
            #矩形の面積を用いた終了判定
            """
            if self.area>self.camera.AREA_THRE_END:
                self.countAreaLoopEnd+=1
                if self.countAreaLoopEnd>self.camera.COUNT_AREA_LOOP_THRE_END:
                    break
            else:
                self.countAreaLoopEnd=0
            """
            
            cv2.rectangle(frame, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), (0, 0, 255), thickness=2) # フレームを生成
            # print (13500//rect[3]) # 距離の概算出力
        
        cv2.drawMarker(frame,(self.camera.cgx,self.camera.cgy),(60,0,0))
        #frame=cv2.flip(frame,0)#上下反転
        frame=cv2.rotate(frame,cv2.ROTATE_180)
        cv2.imshow('red', frame)
        cv2.waitKey(1)
        
        """
        #画面に赤い要素が全くない場合の見失い判定
        if self.following==1 and len(rects)==0:
            self.countAreaLoopLose+=1
            if self.countAreaLoopLose>ct.const.COUNT_AREA_LOOP_THRE_LOSE:
                self.state=0
                self.countAreaLoopLose=0
                self.following=0
                print('見失った2！')
                cv2.destroyAllWindows()
        """

    def finish(self):
        print('finished!')
        self.capture.release()
        cv2.destroyAllWindows()
        sys.exit()


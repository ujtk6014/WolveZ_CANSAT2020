import cv2
#import numpy as np
import sys
import os
import datetime
import constant as ct
import camera

class Cansat(object):
    
    def __init__(self):
        self.countAreaLoopEnd=0 # 終了判定用
        self.countAreaLoopStart=0 # 開始判定用
        self.countAreaLoopLose=0 # 見失い判定用
        self.countDistanceLoopStart=0
        self.countDistanceLoopEnd=0
        
        self.following=0 # state1の中で、カメラによる検知中か追従中かを区別、どちらもカメラを回しながら行いたいため
        
        self.camera=camera.Camera()
        self.timestep = 0

        date = datetime.datetime.now()
        self.filename = '{0:%Y%m%d}'.format(date)
        path = "./TestResult/" + self.filename
        os.makedirs(path, exist_ok=True)

    
    def setup(self):
        #self.camera.setupCamera()#ガンマ補正のためのセットアップ
        pass 

    def run(self):
        self.timestep += 1
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
        
        # 一定間隔で状況を撮影
        if self.timestep%20==0:
            imName='./TestResult/'+self.filename+'/'+ str(self.timestep)+'.jpg'
            cv2.imwrite(imName,frame)
                
        if len(rects) > 0:
            rect = max(rects, key=(lambda x: x[2] * x[3]))  # 最大の矩形を探索
            
            #各パラメータの計算
            self.camera.find_center_of_gravity(rect) # 重心の計算
            self.camera.find_angle(self.camera.cgx) # 角度の計算、絶対値
            self.camera.find_direction(self.camera.cgx) # 進む方向
            self.camera.find_area(rect) # 矩形の面積算出
            
            # #追従開始判定
            # if self.following==0 and self.camera.area>ct.const.AREA_THRE_START:
            #     self.countAreaLoopStart+=1
            #     if self.countAreaLoopStart==1:
            #         self.camera.cgxs=self.camera.cgx
            #         self.camera.cgys=self.camera.cgy
            #     if self.countAreaLoopStart>ct.const.COUNT_AREA_LOOP_THRE_START:
            #         if pow(self.camera.cgx-self.camera.cgxs,2)+pow(self.camera.cgy-self.camera.cgys,2)>ct.const.COG_THRE_START:
            #             print("追従開始")
            #             self.following=1
            #             self.countAreaLoopStart=0
            # else:
            #     self.countAreaLoopStart=0
            
            print("Timestep:" + str(self.timestep))
            if self.camera.direct==0:
                print("right motor:"+ str(100) + "|" + "left motor:"+ str(100))
            
            if self.camera.direct==1:
                print("right motor:"+ str(100) + "|" + "left motor:"+ str(round(100*(1-self.camera.angle/62.2))))

            if self.camera.direct== -1:
                print("right motor:"+ str(round(100*(1-self.camera.angle/62.2))) + "|" + "left motor:"+ str(100))
            

            cv2.rectangle(frame, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), (0, 0, 255), thickness=2) # フレームを生成
            cv2.drawMarker(frame,(self.camera.cgx,self.camera.cgy),(60,0,0))
            # print (13500//rect[3]) # 距離の概算出力
        
        
        
        #frame=cv2.flip(frame,0)#上下反転
        #frame=cv2.rotate(frame,cv2.ROTATE_180)

        cv2.imshow('red', frame)
        cv2.waitKey(1)

import cv2
import numpy as np
import sys

import camera
import ultrasonic
import bno055

class Cansat(object):
    
    def __init__(self):
        self.cgx=0
        self.cgy=0
        self.cgxs=0.0
        self.cgys=0.0
        self.angle=0.0
        self.direct=0
        self.area=0.0
        self.countAreaLoopEnd=0 # 終了判定用
        self.countAreaLoopStart=0 # 開始判定用
        self.countAreaLoopLose=0 # 見失い判定用
        self.dist=0.0
        self.countDistanceLoopStart=0
        self.countDistanceLoopEnd=0
        self.state=0
        self.following=0 # state1の中で、カメラによる検知中か追従中かを区別、どちらもカメラを回しながら行いたいため
        self.cam=camera.Camera()
        self.hcsr=ultrasonic.Ultrasonic()
        self.timestep=0
        self.Bno=bno055.Bno055()

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
        self.Bno.setupBno()

    def sensor(self):
        self.Bno.readlinearaccel()
        self.Bno.readgravity()
        print('Ax=',self.Bno.Ax,',Ay=',self.Bno.Ay,',Az=',self.Bno.Az)
        print('gx=',self.Bno.gx,',gy=',self.Bno.gy,',gz=',self.Bno.gz)

    def waiting(self):
        self.dist=self.hcsr.read_distance()
        if self.dist<self.hcsr.DISTANCE_THRE_START:
            self.countDistanceLoopStart+=1
            if self.countDistanceLoopStart>self.hcsr.COUNT_DISTANCE_LOOP_THRE_START:
                print("対象認知＆カメラ処理開始")
                self.state=1
                self.countDistanceLoopStart=0
        else:
            self.countDistanceLoopStart=0


    def running(self):
        self.capture = cv2.VideoCapture(0)
        while cv2.waitKey(30) < 0:
            #カメラループの中でセンサの値を取得（記録のために必要？）
            #self.sensor()
            
            #写真撮影用
            self.timestep+=1
            
            _, frame = self.capture.read() # 動画の読み込み
            # frame=cv2.resize(frame, (640,480)) # プレビューサイズ（いじらなくてよい）
            rects = self.cam.find_rect_of_target_color(frame) # 矩形の情報作成
            
            # 一定間隔で状況を撮影
            if self.timestep%200==0:
                imName=str(self.timestep)+'image.jpg'
                cv2.imwrite(imName,frame)
            
            if len(rects) > 0:
                rect = max(rects, key=(lambda x: x[2] * x[3]))  # 最大の矩形を探索
                
                #各パラメータの計算
                self.cgx,self.cgy=self.cam.find_center_of_gravity(rect) # 重心の計算
                self.angle=self.cam.find_angle(self.cgx) # 角度の計算、絶対値
                self.direct=self.cam.find_direction(self.cgx) # 進む方向
                self.area=self.cam.find_area(rect) # 矩形の面積算出
                
                #追従開始判定
                if self.following==0 and self.area>self.cam.AREA_THRE_START:
                    self.countAreaLoopStart+=1
                    if self.countAreaLoopStart==1:
                        self.cgxs=self.cgx
                        self.cgys=self.cgy
                    if self.countAreaLoopStart>self.cam.COUNT_AREA_LOOP_THRE_START:
                        if pow(self.cgx-self.cgxs,2)+pow(self.cgy-self.cgys,2)>self.cam.COG_THRE_START:
                            print("追従開始")
                            self.following=1
                            self.countAreaLoopStart=0
                else:
                    self.countAreaLoopStart=0
                
                #モーターへの指示を行う
                if self.following==1:
                    #print('モーターへの指示')
                    if self.direct==0:
                        print('right motor:', 100)
                        print('left motor:', 100)
                    if self.direct==1:
                        print('right motor:', 100*(1-self.angle/180))
                        print('left motor:', 100)
                    if self.direct==-1:
                        print('right motor:', 100)
                        print('left motor:', 100*(1-self.angle/180))
                    #ここにモーターへの指示内容をかく！
                
                #見失い判定
                if self.following==1 and self.area<self.cam.AREA_THRE_LOSE:
                    self.countAreaLoopLose+=1
                    if self.countAreaLoopLose>self.cam.COUNT_AREA_LOOP_THRE_LOSE:
                        self.state=0
                        self.countAreaLoopLose=0
                        self.following=0
                        print('見失った！')
                        self.capture.release()
                        cv2.destroyAllWindows()
                        break
                else:
                    self.countAreaLoopLose=0
              
                #超音波センサを用いた終了判定
                self.dist=self.hcsr.read_distance()
                if self.following==1 and self.dist<self.hcsr.DISTANCE_THRE_END:
                    self.countDistanceLoopEnd+=1
                    if self.countDistanceLoopEnd>self.hcsr.COUNT_DISTANCE_LOOP_THRE_END:
                        print("追従終了")
                        self.state=2
                        break
                else:
                    self.countDistanceLoop=0
                #矩形の面積を用いた終了判定
                """
                if self.area>self.cam.AREA_THRE_END:
                    self.countAreaLoopEnd+=1
                    if self.countAreaLoopEnd>self.cam.COUNT_AREA_LOOP_THRE_END:
                        break
                else:
                    self.countAreaLoopEnd=0
                """
                
                
                
                cv2.rectangle(frame, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), (0, 0, 255), thickness=2) # フレームを生成
                # print (direct)
                # print (angle)
                # print (cgx, cgy) #重心座標の出力
                # print (13500//rect[3]) # 距離の概算出力
            cv2.drawMarker(frame,(self.cgx,self.cgy),(60,0,0))
            cv2.imshow('red', frame)
            
            #画面に赤い要素が全くない場合の見失い判定
            if self.following==1 and len(rects)==0:
                self.countAreaLoopLose+=1
                if self.countAreaLoopLose>self.cam.COUNT_AREA_LOOP_THRE_LOSE:
                    self.state=0
                    self.countAreaLoopLose=0
                    self.following=0
                    print('見失った2！')
                    self.capture.release()
                    cv2.destroyAllWindows()
                    break

    def finish(self):
        print('finished!')
        self.capture.release()
        cv2.destroyAllWindows()
        sys.exit()


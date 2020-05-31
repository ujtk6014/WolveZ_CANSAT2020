import cv2
import numpy as np

import camera
import hcsr04

cgx=0
cgy=0
cgxs=0.0
cgys=0.0
angle=0.0
direct=0
area=0.0
countAreaLoopEnd=0 # 終了判定用
countAreaLoopStart=0 # 開始判定用
dist=0.0
countDistanceLoopStart=0
countDistanceLoopEnd=0
state=0


cam=camera.Camera
hcsr=hcsr04.Hcsr04

while True:
    dist=hcsr.read_distance()
    if state==0 and dist<hcsr.DISTANCE_THRE_START:
        countDistanceLoopStart+=1
        if countDistanceLoopStart>hcsr.COUNT_DISTANCE_LOOP_THRE_START:
            print("対象認知＆カメラ処理開始")
            state=1
            break
    else:
        countDistanceLoopStart=0

capture = cv2.VideoCapture(0)
while cv2.waitKey(30) < 0:
    _, frame = capture.read() # 動画の読み込み
    # frame=cv2.resize(frame, (640,480)) # プレビューサイズ（いじらなくてよい）
    rects = cam.find_rect_of_target_color(frame) # 矩形の情報作成
    if len(rects) > 0:
        rect = max(rects, key=(lambda x: x[2] * x[3]))  # 最大の矩形を探索
        
        cgx,cgy=cam.find_center_of_gravity(rect) # 重心の計算
        angle=cam.find_angle(cgx) # 角度の計算
        direct=cam.find_direction(cgx) # 進む方向
        area=cam.find_area(rect) # 矩形の面積算出
        
        #追従開始判定
        if state==1 and area>cam.AREA_THRE_START:
            countAreaLoopStart+=1
            if countAreaLoopStart==1:
                cgxs=cgx
                cgys=cgy
            if countAreaLoopStart>cam.COUNT_AREA_LOOP_THRE_START:
                if pow(cgx-cgxs,2)+pow(cgy-cgys,2)>cam.COG_THRE_START:
                    print("追従開始")
                    state=2
        else:
            countAreaLoopStart=0
      
        #超音波センサを用いた終了判定
        dist=hcsr.read_distance()
        if dist<hcsr.DISTANCE_THRE_END:
            countDistanceLoopEnd+=1
            if countDistanceLoopEnd>hcsr.COUNT_DISTANCE_LOOP_THRE_END:
                print("追従終了")
                break
        else:
            countDistanceLoop=0
        #矩形の面積を用いた終了判定
        """
        if area>cam.AREA_THRE_END:
            countAreaLoopEnd+=1
            if countAreaLoopEnd>cam.COUNT_AREA_LOOP_THRE_END:
                break
        else:
            countAreaLoopEnd=0
        """
        
        cv2.rectangle(frame, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), (0, 0, 255), thickness=2) # フレームを生成
        # print (direct)
        # print (angle)
        # print (cgx, cgy) #重心座標の出力
        # print (13500//rect[3]) # 距離の概算出力
    cv2.drawMarker(frame,(cgx,cgy),(60,0,0))
    cv2.imshow('red', frame)
capture.release()
cv2.destroyAllWindows()
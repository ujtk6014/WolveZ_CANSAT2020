import cv2
import numpy as np

import camera

cam=camera.Camera

capture = cv2.VideoCapture(0)
while cv2.waitKey(30) < 0:
    _, frame = capture.read() # 動画の読み込み
    # frame=cv2.resize(frame, (640,480)) # プレビューサイズ（いじらなくてよい）
    rects = cam.find_rect_of_target_color(frame) # 矩形の情報作成
    if len(rects) > 0:
      rect = max(rects, key=(lambda x: x[2] * x[3]))  # 最大の矩形を探索
      area=cam.find_area(rect)
      if area>cam.AREA_THRE:
          countAreaLoop+=1
          if countAreaLoop>cam.COUNT_AREA_LOOP_THRE:
              break
      else:
          countAreaLoop=0
      cv2.rectangle(frame, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), (0, 0, 255), thickness=2) # フレームを生成
      cgx,cgy=cam.find_center_of_gravity(rect) # 重心の計算
      angle=cam.find_angle(cgx) # 角度の計算
      direct=cam.find_direction(cgx) # 進む方向
      # print (direct)
      print (angle)
      # print (cgx, cgy) #重心座標の出力
      # print (13500//rect[3]) # 距離の概算出力
    cv2.drawMarker(frame,(cgx,cgy),(60,0,0))
    cv2.imshow('red', frame)
capture.release()
cv2.destroyAllWindows()
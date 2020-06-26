import cv2
import numpy as np

class Camera(object):
    
    #閾値の定義
    AREA_THRE_END=20000
    COUNT_AREA_LOOP_THRE_END=30
    AREA_THRE_LOSE=50
    COUNT_AREA_LOOP_THRE_LOSE=70
    AREA_THRE_START=2500
    COUNT_AREA_LOOP_THRE_START=10
    COG_THRE_START=15000
    
    def __init__(self):
        self.cgx=0
        self.cgy=0
        self.cgxs=0.0
        self.cgys=0.0
        self.angle=0.0
        self.direct=0
        self.area=0.0

    def find_rect_of_target_color(self,image):
      hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV_FULL)
      h = hsv[:, :, 0] # 色相(Hue)                          
      s = hsv[:, :, 1] #彩度(Saturation)
      mask = np.zeros(h.shape, dtype=np.uint8) # 赤いところを示すマスクデータ作成
      mask[((h < 20) | (h > 200)) & (s > 128)] = 255
      # mask[((h < 20) | (h > 200)) & (s > 64)] = 255
      contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # 輪郭を作成
      rects = []
      for contour in contours: # 内包する凸形状を作り、矩形を計算
        approx = cv2.convexHull(contour)
        rect = cv2.boundingRect(approx)
        rects.append(np.array(rect))
      return rects

    def find_center_of_gravity(self,data):
        self.cgx=data[0]+data[2]//2  
        self.cgy=data[1]+data[3]//2

    def find_direction(self,x_coordinate):
        angle=(x_coordinate-320)*31.1/320
        if angle>10:
            self.direct=1 # 右
        elif angle<-10:
            self.direct=-1 # 左
        else:
            self.direct=0# 直進
            
    def find_angle(self,x_coordinate):
        self.angle=abs(x_coordinate-320)*31.1/320
    
    def find_area(self,data):
        self.area=data[2]*data[3]

    """
    def find_rect_of_target_color(image):
      hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV_FULL)
      h = hsv[:, :, 0]
      s = hsv[:, :, 1]
      v = hsv[:, :, 0]
      mask = np.zeros(h.shape, dtype=np.uint8)
      mask[((h < 50) | (h > 200)) & (s > 100)] = 255
      contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
      rects = []
      for contour in contours:
        approx = cv2.convexHull(contour)
        rect = cv2.boundingRect(approx)
        rects.append(np.array(rect))
      return rects

    capture = cv2.VideoCapture(0)
    while cv2.waitKey(30) < 0:
        _, frame = capture.read()
        rects = find_rect_of_target_color(frame)
        for rect in rects:
            cv2.rectangle(frame, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), (0, 0, 255), thickness=2)
            cv2.imshow('red', frame)
    capture.release()
    cv2.destroyAllWindows()
    """

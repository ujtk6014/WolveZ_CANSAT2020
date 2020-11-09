import cv2
import numpy as np
from matplotlib import pylab as plt
import camera

can = camera.Camera()

#使うときは日付と見たい写真を変更する
# date = input('Please input date (ex:20201023):')
date =  '20201028_1'
pic_num = input('enter the picture number:')
pic_num = pic_num + ".jpg"
path = './TestResult/' + date + '/' + pic_num
print(path)
img = cv2.imread(path)
#平滑化
img_hist_eq = img.copy()
img_hist_eq_adap =img.copy()
# plt.subplot(3,1,1)

# 矩形の情報作成
rects = can.find_rect_of_target_color(img)
if len(rects) > 0:
    rect = max(rects, key=(lambda x: x[2] * x[3]))  # 最大の矩形を探索
cv2.rectangle(img, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), (0, 0, 255), thickness=2) 
cv2.imshow('original image',img)
# img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

########################################################################################################
#普通の平坦化
# RGBそれぞれを平坦化
for i in range(3):
    img_hist_eq[:, :, i] = cv2.equalizeHist(img_hist_eq[:, :, i])
    

# 矩形の情報作成
rects = can.find_rect_of_target_color(img_hist_eq)
print(len(rects))
if len(rects) > 0:
    rect = max(rects, key=(lambda x: x[2] * x[3]))  # 最大の矩形を探索

cv2.rectangle(img_hist_eq, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), (0, 0, 255), thickness=2) 
cv2.imshow('converted image',img_hist_eq)


#######################################################################################################
# 適応的平坦化
# RGBそれぞれを適応的に平坦化（８＊８の領域ごとに平坦化していく）
for i in range(3):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    img_hist_eq_adap[:, :, i] = clahe.apply(img_hist_eq_adap[:, :, i])

# 矩形の情報作成
rects = can.find_rect_of_target_color(img_hist_eq_adap)
print(len(rects))
if len(rects) > 0:
    rect = max(rects, key=(lambda x: x[2] * x[3]))  # 最大の矩形を探索

cv2.rectangle(img_hist_eq_adap, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), (0, 0, 255), thickness=2) 
cv2.imshow('adaptive converted image',img_hist_eq_adap)
cv2.waitKey(0) # キー待ち
cv2.destroyAllWindows()

# a = np.array(img_hist_eq)
# plt.imshow(a)
# plt.gray()
# plt.axis('off')

# # 下段のヒストグラムの設定
# plt.subplot(3, 1, 2)
# plt.hist(a.flatten(), bins=np.arange(256 + 1)) #階級の幅を1としてヒストグラムを出す

# plt.subplot(3, 1, 3)
# color = ('b','g','r')
# for i,col in enumerate(color):
#     histr = cv2.calcHist([img_hist_eq],[i],None,[256],[0,256])
#     plt.plot(histr,color = col)
#     plt.xlim([0,256])

plt.show()
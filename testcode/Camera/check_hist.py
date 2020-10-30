import cv2
import numpy as np
from matplotlib import pylab as plt

#使うときは日付と見たい写真を変更する
date = "20201028_1"
pic_num = "520.jpg"
path = './TestResult/' + date + '/' + pic_num
print(path)
img = cv2.imread(path)
cv2.imshow('pic preview',img)
cv2.waitKey(0) # キー待ち
cv2.destroyAllWindows()
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

plt.figure(1)
plt.subplot(3,1,1)
a = np.array(img)
plt.imshow(a)
plt.gray()
plt.axis('off')

# 下段のヒストグラムの設定
plt.subplot(3, 1, 2)
plt.hist(a.flatten(), bins=np.arange(256 + 1)) #階級の幅を1としてヒストグラムを出す

plt.subplot(3, 1, 3)
color = ('b','g','r')
for i,col in enumerate(color):
    histr = cv2.calcHist([img],[i],None,[256],[0,256])
    plt.plot(histr,color = col)
    plt.xlim([0,256])


#平滑化
img_hist_eq = img.copy()
# RGBそれぞれを平坦化
for i in range(3):
    img_hist_eq[:, :, i] = cv2.equalizeHist(img_hist_eq[:, :, i])

plt.figure(2)
plt.subplot(3,1,1)
a = np.array(img_hist_eq)
plt.imshow(a)
plt.gray()
plt.axis('off')

# 下段のヒストグラムの設定
plt.subplot(3, 1, 2)
plt.hist(a.flatten(), bins=np.arange(256 + 1)) #階級の幅を1としてヒストグラムを出す

plt.subplot(3, 1, 3)
color = ('b','g','r')
for i,col in enumerate(color):
    histr = cv2.calcHist([img_hist_eq],[i],None,[256],[0,256])
    plt.plot(histr,color = col)
    plt.xlim([0,256])


#平滑化
img_hist_eq_adap = img.copy()
# RGBそれぞれを適応的に平坦化（８＊８の領域ごとに平坦化していく）
for i in range(3):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    img_hist_eq_adap[:, :, i] = clahe.apply(img_hist_eq_adap[:, :, i])

plt.figure(3)
plt.subplot(3,1,1)
a = np.array(img_hist_eq_adap)
plt.imshow(a)
plt.gray()
plt.axis('off')

# 下段のヒストグラムの設定
plt.subplot(3, 1, 2)
plt.hist(a.flatten(), bins=np.arange(256 + 1)) #階級の幅を1としてヒストグラムを出す

plt.subplot(3, 1, 3)
color = ('b','g','r')
for i,col in enumerate(color):
    histr = cv2.calcHist([img_hist_eq_adap],[i],None,[256],[0,256])
    plt.plot(histr,color = col)
    plt.xlim([0,256])


plt.show()
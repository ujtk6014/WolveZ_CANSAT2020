# -*- coding: utf-8 -*-

import cansat
import cv2
import time
import RPi.GPIO as GPIO
import sys
import constant as ct

can=cansat.Cansat()
can.setup()

try:
    can.capture = cv2.VideoCapture(0)
    frame_rate = 5 # フレームレート
    size = (640, 480) # 動画の画面サイズ
    fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v') # ファイル形式(ここではmp4)
    can.writer = cv2.VideoWriter('./cansat_video.mp4', fmt, frame_rate, size) # ライター作成

    while True:
        can.sensor()
        t1=time.time()
        time.sleep(0.05)
        can.sequence()
        t2=time.time()
        time.sleep(0.05)
#         prints(t2-t1)
except (KeyboardInterrupt,StopIteration):
    print('finished')
    can.writer.release() 
    GPIO.output(ct.const.RELEASING_PIN,0) #焼き切りが危ないのでlowにしておく
    GPIO.cleanup()
    pass
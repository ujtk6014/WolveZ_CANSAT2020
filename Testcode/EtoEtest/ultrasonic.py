#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import constant as ct
import RPi.GPIO as GPIO

class Ultrasonic(object):
    
    def __init__(self):
        self.dist=0.0
        self.count = 0
        # 使用するピンの設定
        GPIO.setmode(GPIO.BCM)
        
        # ピンのモードをそれぞれ出力用と入力用に設定
        GPIO.setup(ct.const.ULTRASONIC_TRIG,GPIO.OUT)
        GPIO.setup(ct.const.ULTRASONIC_ECHO,GPIO.IN)
        GPIO.output(ct.const.ULTRASONIC_TRIG, GPIO.LOW)
        
    # 距離を読む関数
    def getDistance(self):
        # TRIG に短いパルスを送る
        GPIO.output(ct.const.ULTRASONIC_TRIG, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(ct.const.ULTRASONIC_TRIG, GPIO.LOW)
        
        # ECHO ピンがHIGHになるのを待つ
        signaloff = time.time()
        '''
        while GPIO.input(ct.const.ULTRASONIC_ECHO) == GPIO.LOW:
            signaloff=time.time()
            
        while GPIO.input(ct.const.ULTRASONIC_ECHO) == GPIO.HIGH:
            signalon=time.time()
        '''
        
        
        while GPIO.input(ct.const.ULTRASONIC_ECHO) == GPIO.LOW:
            self.count+=1
            #print(str(self.count))
            signaloff = time.time()
            if self.count>500:
                break
        self.count = 0
        # ECHO ピンがLOWになるのを待つ
        signalon = signaloff
        while time.time() < signaloff + 0.1:
            if GPIO.input(ct.const.ULTRASONIC_ECHO) == GPIO.LOW:
                signalon = time.time()
                break
        
        
        
        # GPIO を初期化しておく
        #GPIO.cleanup()
        
        # 時刻の差から、物体までの往復の時間を求め、距離を計算する
        timepassed = signalon - signaloff
        distance = timepassed * 17000
        
        # 500cm 以上の場合はノイズと判断する
        if distance <= 350:#default=350
            #return distance
            self.dist=distance
        else:
            self.dist=500
"""  
ultrasonic=Ultrasonic()
while True:
    ultrasonic.getDistance()
    print(ultrasonic.dist)
    #time.sleep(0.05)
"""
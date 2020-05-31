#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

class Hcsr04(object):
    
    DISTANCE_THRE_START=400.0
    COUNT_DISTANCE_LOOP_THRE_START=40
    DISTANCE_THRE_END=50.0
    COUNT_DISTANCE_LOOP_THRE_END=40
    
    # 距離を読む関数
    def read_distance():
        # 必要なライブラリのインポート・設定
        import RPi.GPIO as GPIO

        # 使用するピンの設定
        GPIO.setmode(GPIO.BCM)
        TRIG = 2 # GPIO02(Pin3)
        ECHO = 3 # GPIO03(Pin5)

        # ピンのモードをそれぞれ出力用と入力用に設定
        GPIO.setup(TRIG,GPIO.OUT)
        GPIO.setup(ECHO,GPIO.IN)
        GPIO.output(TRIG, GPIO.LOW)

        # TRIG に短いパルスを送る
        GPIO.output(TRIG, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(TRIG, GPIO.LOW)

        # ECHO ピンがHIGHになるのを待つ
        signaloff = time.time()
        while GPIO.input(ECHO) == GPIO.LOW:
            signaloff = time.time()

        # ECHO ピンがLOWになるのを待つ
        signalon = signaloff
        while time.time() < signaloff + 0.1:
            if GPIO.input(ECHO) == GPIO.LOW:
                signalon = time.time()
                break

        # GPIO を初期化しておく
        GPIO.cleanup()

        # 時刻の差から、物体までの往復の時間を求め、距離を計算する
        timepassed = signalon - signaloff
        distance = timepassed * 17000

        # 500cm 以上の場合はノイズと判断する
        #if distance <= 500:
            #return distance
        return distance        


        """
        while True:
            start_time = time.time()
            distance = read_distance()
            if distance:
                print "距離: %.1f cm" % (distance)

            # 次のループまでの間sleepする
            wait = start_time + 1 - time.time()
            if wait > 0:
                time.sleep(wait)
        """

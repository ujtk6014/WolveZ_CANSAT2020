#実際にモーター買って試してみないとわからないかも、コードはこれでいけると思うんだけど...

import RPi.GPIO as GPIO
from time import sleep

class motor():
    def __init__(self,pin1,pin2,vref): #各ピンのセットアップ
        p_in1 = pin1 #入力1
        p_in2 = pin2 #入力2
        p_vref = vref #電圧を参照するピン
        GPIO.setmode(GPIO.BCM) 
        GPIO.setup(p_in1, GPIO.OUT)
        GPIO.setup(p_in2, GPIO.OUT)
        GPIO.setup(p_vref, GPIO.OUT)
        pwmR = GPIO.PWM(p_vref,50) #電圧を参照するピンを周波数50HZに指定（Arduinoはデフォルトで490だけど、ラズパイはネットだと50HZがメジャーそうだった）

#正転
    def go(self,v):
        if v>100:
            v=0
        if v<0:
            v=0 #vに辺な値があった時の処理のための4行,backのも同じ
        speed=v #vは0から100のDuty比、速度を表す指標として利用、後々stopslowlyで使用
        pwmR.ChangeDutyCycle(v) #Duty比の指定、以下同様
        GPIO.output(in1,1)
        GPIO.output(in2,0)
        
#逆転        
    def back(self,v):
        if v>100:
            v=0
        if v<0:
            v=0
        speed=-v
        pwmR.ChangeDutyCycle(v)
        GPIO.output(in1,0)
        GPIO.output(in2,1)
        
#回転ストップ
    def stop(self):
        speed=0
        pwmR.ChangeDutyCycle(0)
        GPIO.output(in1,0)
        GPIO.output(in2,0)
        
#徐々に回転遅くして最終的にストップ
    def stopslowly(self):
        if not speed==0:
            for _speed in range(speed,0,-10): #少しずつDuty比を落として速度を落とす、-10のところは実験によって変えられそう
                pwmR.ChangeDutyCycle(_speed)
                GPIO.output(in1,1)
                GPIO.output(in2,0)
            speed=0
        pwmR.ChangeDutyCycle(0)
        GPIO.output(in1,0)
        GPIO.output(in2,0)
        
#ブレーキ（何であるんだろう？）
    def brake(self):
        speed=0
        pwmR.ChangeDutyCycle(0)
        GPIO.output(in1,1)
        GPIO.output(in2,1)
"""
Keio Wolve'Z cansat2020
mission function
Author Yuji Tanaka
date:2020/05/26
"""
#ライブラリの読み込み
import time
import RPi.GPIO as GPIO

#クラス読み込み
import constant
import camera
import gps
import motor
import radio
import ultrasonic
import bno055

class Cansat(object):
    #オブジェクトの生成
    cnst = constant.constant()
    rihgtmotor = motor.Motor(cnst.RIGHT_MOTOR_VREF_PIN,cnst.RIGHT_MOTOR_IN1_PIN,cnst.RIGHT_MOTOR_IN2_PIN)
    leftmotor = motor.Motor(cnst.LEFT_MOTOR_VREF_PIN,cnst.LEFT_MOTOR_IN1_PIN,cnst.LEFT_MOTOR_IN2_PIN)
    gps = gps.GPS()
    bno055 = bno055.BNO()
    radio = radio.radio()
    ultrasonic = ultrasonic.Ultrasonic()
    
    def __init__(self):
        #変数
        state = 0
        laststate = 0
        
        #stateに入っている時刻の初期化
        self.state = 0
        self.preparingTime = 0
        self.flyingTime = 0
        self.droppingTime = 0
        self.landingTime = 0
        self.releadingTime = 0
        self.runningTime = 0
        
        #state管理用変数初期化
        self.countPreLoop = 0
        self.countFlyLoop = 0
        self.countDropLoop = 0
        pass
    
    def setup(self):
        gps.setupGps()
        bno055.setupBno()
        radio.setupRadio()
        GPIO.setmode(GPIO.BCM) #enable GPIO
        GPIO.setup(cnst.BURNING_PIN,GPIO.OUT) #using pin 25 as an output
        
    def sensor(self):
    
    def writeSd(self):
    
    def sendLoRa(self):
    
    def sequence(self):
        if state == 0:　#初期化の必要あり
            self.preparing()
        elif state == 1:
            self.flying()
        elif state == 2:
            self.dropping()
        elif state == 3:
            self.landing()
        elif state == 4:
            self.running()
        elif state == 5:
            self.goal()
        else:
            state = 0
    
    def preparing(self):#フライトピンを使う場合はいらないかも
    
    def flying(self):#フライトピンを使う場合はいらないかも
    
    def dropping(self):
        if self.droppingTime == 0:
            self.droppingTime = time.time()#現在の時刻を取得
            
        if (pow(bno055.Ax,2) + pow(bno055.Ay,2) + pow(bno055.Az,2)) < pow(cnst.ACC_THRE,2):#加速度が閾値以下で着地判定
            self.countDropLoop+=1
            if self.countDropLoop > cnst.COUNT_ACC_LOOP_THRE:
                self.state = 3
        else:
            self.countDropLoop = 0 #初期化の必要あり
        """
        #時間で着地判定
        if not self.droppingTime == 0:
            if time.time() - self.droppingTime > cnst.LANDING_TIME_THRE:
                self.state = 3
                self.laststate = 3
        """
        
    def landing(self):
        if self.landingTime == 0:
            self.landingTime = time.time()
            
        GPIO.output(cnst.RELEASING_PIN,HIGH)
        
        if time.time()-self.landingTime > cnst.RELEASING_TIME_THRE:
            GPIO.output(cnst.RELEASING_PIN,LOW)
            self.state = 4
            self.laststate = 4
            
    def running(self):
        if self.runningTime == 0:
            GPIO.output(cnst.RELEASING_PIN,HIGH)
            self.runningTime = time.time()
        
        if self.countRelLoop < cnst.COUNT_REL_LOOP_THRE:
            rightmotor.go() #なにか引数を入れる
            leftmotor.go()
            
    
    def goal(self):
            
        


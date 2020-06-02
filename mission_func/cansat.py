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
import constant as ct
import camera
import gps
import motor
import radio
import ultrasonic
import bno055

class Cansat(object):
    
    def __init__(self):
        #オブジェクトの生成
        self.rihgtmotor = motor.Motor(ct.const.RIGHT_MOTOR_VREF_PIN,ct.const.RIGHT_MOTOR_IN1_PIN,ct.const.RIGHT_MOTOR_IN2_PIN)
        self.leftmotor = motor.Motor(ct.const.LEFT_MOTOR_VREF_PIN,ct.const.LEFT_MOTOR_IN1_PIN,ct.const.LEFT_MOTOR_IN2_PIN)
        self.gps = gps.GPS()
        self.bno055 = bno055.BNO()
        self.radio = radio.radio()
        self.ultrasonic = ultrasonic.Ultrasonic()
        
        #開始時間の記録
        self.startTime = time.time()
        self.timer = 0
        
        #変数
        self.state = 0
        self.laststate = 0
        
        #stateに入っている時刻の初期化
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
        GPIO.setmode(GPIO.BCM) #GPIOの設定
        GPIO.setup(ct.const.BURNING_PIN,GPIO.OUT) #焼き切り用のピンの設定
        
    def sensor(self):
        self.gps.gpsread()
        self.bno055.bnoread()
        self.ultrasonic.distread()
        self.writeData()#txtファイルへのログの保存
        if not self.state == 2:
            self.sendRadio()#LoRaでログを送信
    
    def writeData(self):
        self.timer = 1000*(time.time() - self.startTime) #経過時間 (ms)
        self.timer = int(timer)
        #ログデータ作成。\マークを入れることで改行してもコードを続けて書くことができる
        datalog = str(self.timer) + ","\
                  + str(self.state) + ","\
                  + str(self.gps.Time) + ","\
                  + str(self.gps.Lat) + ","\
                  + str(self.gps.Lon) + ","\
                  + str(self.bno055.gx) + ","\
                  + str(self.bno055.gy) + ","\
                  + str(self.bno055.gz) + ","\
                  + str(self.bno055.Ax) + ","\
                  + str(self.bno055.Ay) + ","\
                  + str(self.bno055.Az) + ","\
                  + str(self.ultrasonic.distance) + ","\
                  + str(self.rightmotor.velocity) + ","\
                  + str(self.leftmotor.velocity)
        
        with open("test.txt",mode = 'a') as test: # [mode] x:ファイルの新規作成、r:ファイルの読み込み、w:ファイルへの書き込み、a:ファイルへの追記
            test.write(datalog + '\n')
          
    def sendRadio(self):
        datalog = str(self.timer) + ","\
                  + str(self.state) + ","\
                  + str(self.gps.Time) + ","\
                  + str(self.gps.Lat) + ","\
                  + str(self.gps.Lon) + ","\
                  + str(self.bno055.gx) + ","\
                  + str(self.bno055.gy) + ","\
                  + str(self.bno055.gz) + ","\
                  + str(self.ultrasonic.distance) + ","\
                  + str(self.rightmotor.velocity) + ","\
                  + str(self.leftmotor.velocity)
        self.radio.sendData(datalog) #データを送信
    
    def sequence(self):
        if self.state == 0:　#初期化の必要あり
            self.preparing()
        elif self.state == 1:
            self.flying()
        elif self.state == 2:
            self.dropping()
        elif self.state == 3:
            self.landing()
        elif self.state == 4:
            self.waiting()
        elif self.state == 5:
            self.running()
        elif self.state == 6:
            self.goal()
        else:
            self.state = self.laststate #どこにも引っかからない場合何かがおかしいのでlaststateに戻してあげる
    
    def preparing(self):#フライトピンを使う場合はいらないかも
    
    def flying(self):#フライトピンを使う場合はいらないかも
    
    def dropping(self):
        if self.droppingTime == 0:
            self.droppingTime = time.time()#現在の時刻を取得
            
        if (pow(bno055.Ax,2) + pow(bno055.Ay,2) + pow(bno055.Az,2)) < pow(self.ACC_THRE,2):#加速度が閾値以下で着地判定
            self.countDropLoop+=1
            if self.countDropLoop > ct.const.COUNT_ACC_LOOP_THRE:
                self.state = 3
                self.laststate = 3
        else:
            self.countDropLoop = 0 #初期化の必要あり
        """
        #時間で着地判定
        if not self.droppingTime == 0:
            if time.time() - self.droppingTime > ct.const.LANDING_TIME_THRE:
                self.state = 3
                self.laststate = 3
        """
        
    def landing(self):
        if self.landingTime == 0:
            self.landingTime = time.time()
            
        GPIO.output(self.RELEASING_PIN,HIGH)
        
        if time.time()-self.landingTime > ct.const.RELEASING_TIME_THRE:
            GPIO.output(ct.const.RELEASING_PIN,LOW)
            self.state = 4
            self.laststate = 4
            
    def waiting(self):
        
    
    def running(self):
        if self.runningTime == 0:
            GPIO.output(ct.const.RELEASING_PIN,HIGH)
            self.runningTime = time.time()
        
        if self.countRelLoop < ct.const.COUNT_REL_LOOP_THRE:
            rightmotor.go() #なにか引数を入れる
            leftmotor.go()
            
    
    def goal(self):
            
        
if __name__ == "__main__":
    pass

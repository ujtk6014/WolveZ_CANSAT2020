import RPi.GPIO as GPIO         #ラズパイのGPIOライブラリインポート
from time import sleep
from time import time

def setmode():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

class Ultrasonic(object):
    def __init__(self):
        pass
    
    def trig_setup(self,num): #BMC trigpin(17)を出力に設定
        self.trigpin=num 
        GPIO.setup(self.trigpin,GPIO.OUT)
        global trigpin #getDistanceで使えるように
        trigpin=self.trigpin
        
    def echo_setup(self,num): #BMC echopin(18)を入力に設定
        self.echopin=num
        GPIO.setup(self.echopin,GPIO.IN)
        global echopin #getDistanceで使えるように
        echopin=self.echopin
    
    #距離の計算 cm単位
def getDistance():
    GPIO.output(trigpin,GPIO.HIGH)   #trigpin番ピンオン
    sleep(0.00001)         #10us停止
    GPIO.output(trigpin,GPIO.LOW)    #trigpin番ピンオフ
    while GPIO.input(echopin) == 0:
        signaloff = time()
    while GPIO.input(echopin) == 1:
        signalon = time() 
    pulseTime = signalon - signaloff #帰ってくるまでの時間を計算
    distance = pulseTime * 340 / 2 * 100            #音速340m/sで距離を計算
    if distance <= 500:
        return distance  #距離(cm単位)を返す
    else:
        return None
 
    
def loop():
    while True:
        distance = getDistance()
        if distance:
            print ("現在の距離 ： %.3f cm"%(distance))  #コンソールに距離を表示
        sleep(1)    #   
 
 
#「ctrl + C」が押された時(setupとloopで例外が発生した時）の処理
def end():
    print ('「CTRL + C」が入力されたので終了します。')                #コンソールにメッセージを出力
    GPIO.cleanup()              #GPIOをクリア。つけないと警告が出る
 

    
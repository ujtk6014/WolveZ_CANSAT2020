
import time
import RPi.GPIO as GPIO
 
time.sleep(2)
 
print('テスト開始')
 
# GPIOの基本的な設定
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
 
GPIO.setup(8,  GPIO.OUT)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
 
pwmR = GPIO.PWM(12, 50) # 周波数50Hz　デューティー比0%でPWM出力　オブジェクト作成
pwmR.start(0)
 
print('正転')
pwmR.ChangeDutyCycle(0)
GPIO.output(8,  1)
GPIO.output(10, 0)
 
print ' 30'
pwmR.ChangeDutyCycle(30)
time.sleep(2)
print ' 60'
pwmR.ChangeDutyCycle(60)
time.sleep(2)
print ' 100'
pwmR.ChangeDutyCycle(100)
time.sleep(2)
 
print 'ストップ'
GPIO.output(8,  0)
GPIO.output(10, 0)
time.sleep(2)
 
print ('逆転')
pwmR.ChangeDutyCycle(0)
GPIO.output(8,  0)
GPIO.output(10, 1)
 
print (' 30')
pwmR.ChangeDutyCycle(30)
time.sleep(2)
print ' 60'
pwmR.ChangeDutyCycle(60)
time.sleep(2)
print ' 100'
pwmR.ChangeDutyCycle(100)
time.sleep(2)
 
print ('ブレーキ')
GPIO.output(8, 1)
GPIO.output(10, 1)
time.sleep(1)
 
# GPIO後処理
GPIO.output(8, 0)
GPIO.output(10, 0)
pwmR.stop()
 
GPIO.cleanup()
time.sleep(1)
 
print 'テスト終了'
# -*- coding: utf-8 -*-
'''
2020.03.21
버튼이 눌리면 firebase database에 있는 'Request' 값을 1로 바꾸고,
firebase database의 Request 값이 1인 차량 번호를 불러온다.
'''

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
# red_led = port 12
GPIO.setup(12, GPIO.OUT)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)

db_url = 'https://whoru-ed991.firebaseio.com/'
cred = credentials.Certificate("myKey.json")
db_app = firebase_admin.initialize_app(cred, {'databaseURL': db_url})
ref = db.reference()

pin_servo_motor = 18 # GPIO.BCM 18
#pin_servo_motor = 12 # GPIO.BOARD
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_servo_motor, GPIO.OUT)

p = GPIO.PWM(pin_servo_motor, 50)
p.start(0)

cnt = 0

pwm = 0

switch = 0

try:
    while True:
        input_state = GPIO.input(11)
        if input_state == 1:
            if switch == 0:
                switch = 1
                ref.child("carlist/06수 8850").update({'Request': '1'})
            else:
                switch = 0
                ref.child("carlist/06수 8850").update({'Request': '0'})

        flag = ref.child("carlist/06수 8850/approved").get()
        if flag == 1:
            # led off
            GPIO.output(12, GPIO.LOW)
            # motor on
            pwm = input()
            pwm = int(pwm)
            p.ChangeDutyCycle(pwm)
            print("angle : {}".format(pwm))
            time.sleep(0.5)
        else: GPIO.output(12, GPIO.HIGH)

        '''
        pwm += 1
        if pwm == 10:
            pwm = 0
        '''
except KeyboardInterrupt:
    p.stop()
GPIO.cleanup()

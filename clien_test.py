import RPi.GPIO as GPIO
import socket
import time

GPIO.setwarnings(False)  # disable warning about used port
GPIO.setmode(GPIO.BCM)  # set mode, how to name pins
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # set port of button
GPIO.setup(12, GPIO.OUT)  # set LED

s = socket.socket()  # create socket
host = '192.168.155.213'  # ip of host
port = 12345  # port
s.connect((host, port))


def send():
    s.sendto(b'1', (host, port))  #


while True:
    if GPIO.input(17) == GPIO.HIGH:
        GPIO.output(12, GPIO.HIGH)
        time.sleep(0.2)
        s.sendto(b'1', (host, port))  #
    else:
        # print("Button not pushed")
        GPIO.output(12, GPIO.LOW)
        s.sendto(b'0', (host, port))  #
        time.sleep(0.2)


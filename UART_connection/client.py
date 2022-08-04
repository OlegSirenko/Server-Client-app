import serial
import socket
import time
import RPi.GPIO as GPIO

btSerial = serial.Serial("/dev/rfcomm0", baudrate=9600, timeout=1)

GPIO.setwarnings(False)  # disable warning about used port
GPIO.setmode(GPIO.BCM)  # set mode, how to name pins
GPIO.setup(12, GPIO.OUT)  # set LED

s = socket.socket()  # create socket
host = '192.168.110.213'  # ip of host
port = 12345  # port
s.connect((host, port))

while True:
    rcv = btSerial.read(512)
    if rcv:
        btSerial.write(b"OK!\n")  # answer to message to understand that message caught
        print(rcv)
        GPIO.output(12, GPIO.HIGH)  # make LED shine while message is sending with socket connection
        s.sendto(rcv, (host, port))  # sending message
        time.sleep(0.1)  # COULD BE REMOVED. Some timeout to see LED shining
        GPIO.output(12, GPIO.LOW)  # turn off LED when message sent


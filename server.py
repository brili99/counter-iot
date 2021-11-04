import RPi.GPIO as GPIO
import mysql.connector
from time import sleep

mydb = mysql.connector.connect(
    host="localhost",
    user="counter",
    password="bismillah",
    database="tppri_counter"
)

pin_btn1 = 11
pin_btn2 = 5
pin_btn3 = 6
pin_btn4 = 13
pin_btn5 = 19
pin_btn6 = 26

pin_led_red = 24
pin_led_green = 23
pin_led_yellow = 18

pin_sound_1 = 7
pin_sound_2 = 8
pin_sound_3 = 25

pin_driver_1 = 21
pin_driver_2 = 20
pin_driver_3 = 16

pin_relay = 12

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_btn1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin_btn2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin_btn3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin_btn4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin_btn5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin_btn6, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.setup(pin_led_red, GPIO.OUT)
GPIO.setup(pin_led_green, GPIO.OUT)
GPIO.setup(pin_led_yellow, GPIO.OUT)

GPIO.setup(pin_sound_1, GPIO.OUT)
GPIO.setup(pin_sound_2, GPIO.OUT)
GPIO.setup(pin_sound_3, GPIO.OUT)

GPIO.setup(pin_driver_1, GPIO.OUT)
GPIO.setup(pin_driver_2, GPIO.OUT)
GPIO.setup(pin_driver_3, GPIO.OUT)

GPIO.setup(pin_relay, GPIO.OUT)

btn1 = GPIO.input(pin_btn1)
btn2 = GPIO.input(pin_btn2)
btn3 = GPIO.input(pin_btn3)
btn4 = GPIO.input(pin_btn4)
btn5 = GPIO.input(pin_btn5)
btn6 = GPIO.input(pin_btn6)


def add_counter(nmr_btn):
    mycursor = mydb.cursor(buffered=True , dictionary=True)
    mycursor.execute("SHOW TABLES LIKE 'status'")
    if mycursor.rowcount == 0:
        print("tables status is missing, creating table now")
        import os
        os.system('php api/conn.php')
        sleep(0.5)
        # return
    print("adding counter")
    mycursor.execute("SELECT counter FROM status WHERE btn='"+str(nmr_btn)+"'")
    myresult = mycursor.fetchall()
    # print(myresult[0]["counter"])
    counter = int(myresult[0]["counter"]) + 1
    mycursor.execute("UPDATE status SET counter='" +
                     str(counter)+"' WHERE btn='"+str(nmr_btn)+"'")
    mydb.commit()
    if mycursor.rowcount > 0:
        print("success adding counter btn "+str(nmr_btn))
    else:
        print("fail addding counter btn "+str(nmr_btn))
    mycursor.close()
    
def do_loop():
    print("server is ready.")
    while True:
        # print("waiting")
        GPIO.output(pin_sound_1, GPIO.HIGH)
        GPIO.output(pin_sound_2, GPIO.HIGH)
        GPIO.output(pin_sound_3, GPIO.HIGH)
        if GPIO.input(pin_btn1) == 0:
            GPIO.output(pin_led_red, GPIO.HIGH)
            GPIO.output(pin_driver_3, GPIO.HIGH)
            while GPIO.input(pin_btn1) != 1:
                sleep(0.01)
            GPIO.output(pin_led_red, GPIO.LOW)
            GPIO.output(pin_driver_3, GPIO.LOW)
            add_counter(int(1))
        if GPIO.input(pin_btn2) == 0:
            GPIO.output(pin_led_green, GPIO.HIGH)
            GPIO.output(pin_driver_2, GPIO.HIGH)
            while GPIO.input(pin_btn2) != 1:
                sleep(0.01)
            GPIO.output(pin_led_green, GPIO.LOW)
            GPIO.output(pin_driver_2, GPIO.LOW)
            add_counter(int(2))
        if GPIO.input(pin_btn3) == 0:
            GPIO.output(pin_led_yellow, GPIO.HIGH)
            GPIO.output(pin_relay, GPIO.HIGH)
            GPIO.output(pin_driver_1, GPIO.HIGH)
            while GPIO.input(pin_btn3) != 1:
                sleep(0.01)
            GPIO.output(pin_led_yellow, GPIO.LOW)
            GPIO.output(pin_relay, GPIO.LOW)
            GPIO.output(pin_driver_1, GPIO.LOW)
            add_counter(int(3))
        if GPIO.input(pin_btn4) == 0:
            GPIO.output(pin_sound_1, GPIO.HIGH)
            GPIO.output(pin_sound_2, GPIO.LOW)
            GPIO.output(pin_sound_3, GPIO.LOW)
            while GPIO.input(pin_btn4) != 1:
                sleep(0.01)
            add_counter(int(4))
        if GPIO.input(pin_btn5) == 0:
            GPIO.output(pin_sound_1, GPIO.LOW)
            GPIO.output(pin_sound_2, GPIO.HIGH)
            GPIO.output(pin_sound_3, GPIO.LOW)
            while GPIO.input(pin_btn5) != 1:
                sleep(0.01)
            add_counter(int(5))
        if GPIO.input(pin_btn6) == 0:
            GPIO.output(pin_sound_1, GPIO.LOW)
            GPIO.output(pin_sound_2, GPIO.LOW)
            GPIO.output(pin_sound_3, GPIO.HIGH)
            while GPIO.input(pin_btn6) != 1:
                sleep(0.01)
            add_counter(int(6))
        sleep(0.1)
    
# do_loop()
try:
    do_loop()
except:
    print("An exception occurred")

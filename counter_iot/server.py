import RPi.GPIO as GPIO
import mysql.connector
from time import sleep

mydb = mysql.connector.connect(
    host="localhost",
    user="pi",
    password="raspberry",
    database="counter_iot"
)

pin_btn1 = 14
pin_btn2 = 15
pin_btn3 = 22
pin_btn4 = 23
pin_btn5 = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_btn1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin_btn2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin_btn3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin_btn4, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(pin_btn5, GPIO.IN, pull_up_down=GPIO.PUD_UP)

btn1 = GPIO.input(pin_btn1)
btn2 = GPIO.input(pin_btn2)
btn3 = GPIO.input(pin_btn3)
btn4 = GPIO.input(pin_btn4)
btn5 = GPIO.input(pin_btn5)


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
    while True:
        # print("waiting")
        if GPIO.input(pin_btn1) == 0:
            # print("triggered")
            while GPIO.input(pin_btn1) != 1:
                sleep(0.01)
            add_counter(int(1))
        if GPIO.input(pin_btn2) == 0:
            while GPIO.input(pin_btn2) != 1:
                sleep(0.01)
            add_counter(int(2))
        if GPIO.input(pin_btn3) == 0:
            while GPIO.input(pin_btn3) != 1:
                sleep(0.01)
            add_counter(int(3))
        if GPIO.input(pin_btn4) == 0:
            while GPIO.input(pin_btn4) != 1:
                sleep(0.01)
            add_counter(int(4))
        if GPIO.input(pin_btn5) == 0:
            while GPIO.input(pin_btn5) != 1:
                sleep(0.01)
            add_counter(int(5))
        sleep(1)
    
do_loop()
# try:
#     do_loop()
# except:
#     print("An exception occurred")

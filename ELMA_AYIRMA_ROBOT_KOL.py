import cv2
import numpy as np
import time
import RPi.GPIO as GPIO
cap = cv2.VideoCapture(0)
sensor=4
band=17
led_red=22
led_rgb=27


GPIO.setmode(GPIO.BCM)
GPIO.setup(sensor,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(band,GPIO.OUT)
GPIO.setup(led_red,GPIO.OUT)
GPIO.setup(led_rgb,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(24,GPIO.OUT)
GPIO.setup(25,GPIO.OUT)

doner=GPIO.PWM(23,180)
sol=GPIO.PWM(25,180)
sag=GPIO.PWM(18,180)
grip=GPIO.PWM(24,180)
GPIO.output(band,GPIO.LOW)
GPIO.output(led_red,GPIO.LOW)
GPIO.output(led_rgb,GPIO.LOW)

doner.start(10)
sag.start(18)
sol.start(40)
grip.start(15)
time.sleep(1)
GPIO.cleanup()

def go_home(timerhome):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18,GPIO.OUT)
    GPIO.setup(23,GPIO.OUT)
    GPIO.setup(24,GPIO.OUT)
    GPIO.setup(25,GPIO.OUT)
    doner.start(10)
    time.sleep(timerhome)
    sag.start(18)
    time.sleep(timerhome)
    sol.start(40)
    time.sleep(timerhome)
    grip.start(15)
    time.sleep(timerhome)
    GPIO.cleanup()

def elma_al(timer0):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18,GPIO.OUT)
    GPIO.setup(23,GPIO.OUT)
    GPIO.setup(24,GPIO.OUT)
    GPIO.setup(25,GPIO.OUT)
    doner.start(10)
    time.sleep(timer0)
    sol.start(9)
    time.sleep(timer0)
    sag.start(25)
    time.sleep(timer0)
    grip.start(15)
    time.sleep(timer0)
    grip.start(1)
    time.sleep(timer0)
    GPIO.cleanup()
    
def saglama_git(timer1):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18,GPIO.OUT)
    GPIO.setup(23,GPIO.OUT)
    GPIO.setup(24,GPIO.OUT)
    GPIO.setup(25,GPIO.OUT)
    sol.start(35)
    time.sleep(timer1)
    sag.start(30)
    time.sleep(timer1)
    doner.start(8)
    time.sleep(timer1)
    grip.start(15)
    time.sleep(timer1)
    GPIO.cleanup()
    
def curuge_git(timer2):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18,GPIO.OUT)
    GPIO.setup(23,GPIO.OUT)
    GPIO.setup(24,GPIO.OUT)
    GPIO.setup(25,GPIO.OUT)
    sol.start(35)
    time.sleep(timer2)
    sag.start(30)
    time.sleep(timer2)
    doner.start(13)
    time.sleep(timer2)
    grip.start(15)
    time.sleep(timer2)
    GPIO.cleanup()
try:
    while(1):
        cap.set(3,640)
        cap.set(4,480)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(sensor,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(band,GPIO.OUT)
        GPIO.setup(led_red,GPIO.OUT)
        GPIO.setup(led_rgb,GPIO.OUT)

        GPIO.output(band,GPIO.HIGH)
        a=1
        b=1
        # Take each frame
        _, frame = cap.read()
        _, frame1 = cap.read()

        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        hsv1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
   

        # define range of blue color in HSV
        lower_crk = np.array([0,0,0])
        upper_crk = np.array([10,50,50])

    
        lower_saglam = np.array([0,50,50])
        upper_saglam = np.array([10,255,255])


        # Threshold the HSV image to get only blue colors
        mask = cv2.inRange(hsv, lower_crk, upper_crk)
        mask = cv2.erode(mask,None,iterations=2)
        mask = cv2.dilate(mask,None,iterations=2)
    
        mask1= cv2.inRange(hsv1, lower_saglam, upper_saglam)
        mask1 = cv2.erode(mask1,None,iterations=2)
        mask1 = cv2.dilate(mask1,None,iterations=2)
    


        # Bitwise-AND mask and original image
        res = cv2.bitwise_and(frame,frame, mask= mask)
        mask = cv2.GaussianBlur(mask, (3, 3), 0)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    
        mask1 = cv2.GaussianBlur(mask1, (3, 3), 0)
        cnts1 = cv2.findContours(mask1.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    

        if len(cnts)>0:
        
            GPIO.output(led_red,GPIO.HIGH)
            print("CURUK ELMA")
            while(a==1):
                butonOku=GPIO.input(sensor)
                if butonOku==False:
                    GPIO.output(band,GPIO.LOW)
                    GPIO.output(led_red,GPIO.LOW)
                    print("CURUGE GİTTİ")
                    time.sleep(2)
                    elma_al(1)
                    time.sleep(1)
                    curuge_git(1)
                    time.sleep(1)
                    go_home(1)
                    time.sleep(1)
                    a=0
            
                
        if len(cnts1)>0:
            GPIO.output(led_rgb,GPIO.HIGH)
            print("SAGLAM ELMA")
            while(b==1):
                butonOku=GPIO.input(sensor)
                if butonOku==False:
                    GPIO.output(band,GPIO.LOW)
                    GPIO.output(led_rgb,GPIO.LOW)
                    print("SAGLAMA GİTTİ")
                    time.sleep(2)
                    elma_al(1)
                    time.sleep(1)
                    saglama_git(1)
                    time.sleep(1)
                    go_home(1)
                    time.sleep(1)
                    b=0
         

        #cv2.imshow('frame',frame)
        #cv2.imshow('mask',mask)
        #cv2.imshow('res',res)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
  
except KeyboardInterrupt:
    GPIO.cleanup()  

       

cv2.destroyAllWindows()

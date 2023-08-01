from machine import Pin
from neopixel import NeoPixel
import time
from machine import Timer
from CONFIG import *

count = 0
pin=2
rgb_num=24
rgb_led=NeoPixel(Pin(pin,Pin.OUT),rgb_num)

def time0_irq(time0):
    global count, rgb_led
    count += 1
    if count == 24:
        rgb_led[(count+6)%24] = (255,255,255)
        time0.deinit()
    else:
        g = 255*count//23
        rgb_led[(30-count)%24] = (255-g,g,0)
    rgb_led.write()

def ShowBootMsg(period=20):
    global count, rgb_led
    count = 0
    time0=Timer(0)  #创建time0定时器对象
    time0.init(period=period,mode=Timer.PERIODIC,callback=time0_irq)
    
def EndDisp():
    print("dd")
    global rgb_led,rgb_num
    for i in range(24):
        rgb_led[i] = (0,0,0)
    rgb_led.write()
    
def NeoTimeDisp(Time:list):
    hour = Time[4]
    minute = Time[5]
    sec = Time[6]
    min_sec = sec + minute*60
    hourIndex = (29-hour)%24
    minIndex = (29-((24*min_sec)//3600))%24
    minLeft_sec = min_sec-(24*min_sec)//3600
    secIndex = (28-int((24*(minLeft_sec))//150) )%24

    for i in range(24):
        rgb_led[i] = (0,0,0)

    rgb_led[hourIndex] = HPIN
    rgb_led[minIndex] = MPIN
    rgb_led[secIndex] = SPIN
    rgb_led.write()

if __name__ == "__main__":
    ShowBootMsg()
    time.sleep_ms(2500)
    EndDisp()
    
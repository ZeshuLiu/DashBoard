from machine import Pin
from neopixel import NeoPixel
import time
import random
from machine import Timer

count = 0
pin=2
rgb_num=24
rgb_led=NeoPixel(Pin(pin,Pin.OUT),rgb_num)

def time0_irq(time0):
    global count, rgb_led
    count += 1
    if count == 24:
        rgb_led[(count+5)%24] = (255,255,255)
        time0.deinit()
    else:
        g = 255*count//23
        rgb_led[(count+5)%24] = (255-g,g,0)
    rgb_led.write()

def ShowBootMsg():
    global count, rgb_led
    count = 0
    time0=Timer(0)  #创建time0定时器对象
    time0.init(period=80,mode=Timer.PERIODIC,callback=time0_irq)
    
def EndDisp():
    print("dd")
    global rgb_led,rgb_num
    for i in range(24):
        rgb_led[i] = (0,0,0)
    rgb_led.write()
    

if __name__ == "__main__":
    ShowBootMsg()
    time.sleep_ms(2500)
    EndDisp()
    
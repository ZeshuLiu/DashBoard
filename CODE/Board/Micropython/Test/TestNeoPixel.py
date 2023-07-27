
#接线： WS-->(27)
#ADC引脚：33、32、35
 
#导入Pin模块
from machine import Pin
from neopixel import NeoPixel
import time
import random
from machine import ADC
from machine import Timer
 
#定义RGB控制对象
#控制引脚为16，RGB灯串联5个
pin=2
rgb_num=24
rgb_led=NeoPixel(Pin(pin,Pin.OUT),rgb_num)

global a,b,c
a=0
b=0
c=0
 
#定时器0中断函数
def time0_irq(time0):
    global a,b,c
    a+=10
    b+=15
    c+=20
    for i in range(rgb_num):
                rgb_led[i]=(a, b, c)
                rgb_led.write()
                
#程序入口
if __name__=="__main__" :
    time0=Timer(0)  #创建time0定时器对象
    time0.init(period=20,mode=Timer.PERIODIC,callback=time0_irq)
    while True:
        
        pass
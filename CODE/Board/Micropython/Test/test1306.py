from machine import Pin, I2C
from src.bsp.ssd1306_font.ssd1306 import SSD1306_I2C
from src.bsp.ssd1306_font.font import Font
import time

i2c = I2C(0,scl=Pin(22), sda=Pin(21))  #SDA和SCL引脚初始化
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)
f=Font(oled)


f.text("8",0,0,8) #8 pix
f.text("16",8,0,16) #16 pix
f.text("24",24,0,24) #24 pix
f.text("32",48,0,32) #32 pix
f.show()

time.sleep_ms(1000)
def Move(str):
    for i in range(0,128):
        oled.fill(0)
        f.text(str,i,0,16)
        f.text(str,i-128,0,16)
        f.show()
    
while True:
    Move('hello world!')   #原理是指定两个起始符，两个起始符间距刚好是128



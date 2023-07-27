from machine import Pin, I2C
from src.bsp.ssd1306_font.ssd1306 import SSD1306_I2C
from src.bsp.ssd1306_font.font import Font
import time,framebuf

oled_width = 128
oled_height = 64

def ShowBootMsg(display = SSD1306_I2C(oled_width, oled_height, I2C(0,scl=Pin(22), sda=Pin(21))) ):
    with open('./src/usr/pic/pymadethis.pbm', 'rb') as f:
        f.readline() # Magic number
        f.readline() # Creator comment
        f.readline() # Dimensions
        data = bytearray(f.read())
    fbuf = framebuf.FrameBuffer(data, 128, 64, framebuf.MONO_HLSB)
    display.invert(1)
    display.blit(fbuf, 0, 0)           # draw on top at x=10, y=10, key=0
    display.show()

def ShowLogo(display = SSD1306_I2C(oled_width, oled_height, I2C(0,scl=Pin(22), sda=Pin(21))) ):
    display.fill(0)
    display.fill_rect(0, 0, 32, 32, 1)
    display.fill_rect(2, 2, 28, 28, 0)
    display.vline(9, 8, 22, 1)
    display.vline(16, 2, 22, 1)
    display.vline(23, 8, 22, 1)
    display.fill_rect(26, 24, 2, 4, 1)
    display.text('MicroPython', 40, 0, 1)
    display.text('SSD1306', 40, 12, 1)
    display.text('OLED 128x64', 40, 24, 1)
    display.show()
    
def ShowPic(display = SSD1306_I2C(oled_width, oled_height, I2C(0,scl=Pin(22), sda=Pin(21)))):
    with open('./src/usr/pic/tt.pbm', 'rb') as f:
        f.readline() # Magic number
        f.readline() # Creator comment
        #f.readline() # Dimensions
        data = bytearray(f.read())
    fbuf = framebuf.FrameBuffer(data, 128, 64, framebuf.MONO_HLSB)
    display.invert(1)
    display.blit(fbuf, 0, 0)           # draw on top at x=10, y=10, key=0
    display.show()
    
def EndDisp(display = SSD1306_I2C(oled_width, oled_height, I2C(0,scl=Pin(22), sda=Pin(21)))):
    display.fill(0)
    display.poweroff()
    
    
    
if __name__ == "__main__":
    ShowBootMsg()
    ShowLogo()
    ShowPic()
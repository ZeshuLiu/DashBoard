from machine import Pin, I2C
from src.bsp.ssd1306_font.ssd1306 import SSD1306_I2C, SSD1306
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
    display.show()
    #display.poweroff()
    
def Show_Temp_Hum_Date(temp, hum, date_time, display = SSD1306_I2C(oled_width, oled_height, I2C(0,scl=Pin(22), sda=Pin(21)))):
    Month = {1:"Jan", 2:"Feb", 3:"Mar", 4:"Apr" , 5:"May", 6:"Jun", 7:"Jul", 8:"Aug", 9:"Sept", 10:"Oct", 11:"Nov", 12:"Dec"}
    display.invert(0)
    display.fill(0)
    display.rect(0,25,128,10,1,True)
    display.vline(64, 25, 10, 0)
    display.text("TEMP",16, 27,0)
    display.text("HUM",84, 27,0)

    display.vline(64, 35, 29, 1)
    font=Font(display)
    temp_word = str(temp)
    temp_x = 3+(64-16*len(temp_word))//2
    if len(temp_word)<2:
        temp_x-=3
    hum_word = str(hum) + "%"
    hum_x = 72+(64-16*len(hum_word))//2
    font.text(temp_word,temp_x,40,24)
    font.text(hum_word,hum_x,40,24)

    #display.vline(64, 0, 24, 1)
    MD_word = Month[date_time[1]] + ':'
    if date_time[2] <10:
        MD_word += '0'
    MD_word += str(date_time[2])
    font.text(MD_word,2,4,16)
    display.show()


if __name__ == "__main__":
    #ShowBootMsg()
    #ShowLogo()
    #ShowPic()
    for i in range(-50,51):
        Show_Temp_Hum(i,i+50)
        time.sleep_ms(5)
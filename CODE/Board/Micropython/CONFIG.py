BOARD_VER = const(1)

#定义数码管亮度
SEG_Bright = 2 #0-7

#定义主程序刷新速度
MainWorkGap = 100

#定义改变功能后显示时间
ModeChangeDispTime_ms = 1000

#定义检测温湿度间隔
DHT11MesureGap_ms = 5000

#定义引脚
CTRL_PIN = const(23)
BOOT_PIN = const(0)
ENC1A_PIN = const(19)
ENC1B_PIN = const(13)
ENC2A_PIN = const(34)
ENC2B_PIN = const(35)

#防抖时间
DebonuceTime = const(30)

#模拟时钟颜色
R_Brightness = 0.2
G_Brightness = 0.1
B_Brightness = 0.2
HPIN = (int(255*R_Brightness),0,0)
MPIN = (0,int(255*G_Brightness),0)
SPIN = (0,0,int(255*B_Brightness))

if __name__ == "__main__":
    print(BOARD_VER)

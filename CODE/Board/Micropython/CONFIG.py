BOARD_VER = const(1)

#定义引脚
CTRL_PIN = const(23)
BOOT_PIN = const(0)
ENC1A_PIN = const(19)
ENC1B_PIN = const(13)
ENC2A_PIN = const(34)
ENC2B_PIN = const(35)

#防抖时间
DebonuceTime = const(10)

#模拟时钟颜色
HPIN = (255,0,0)
MPIN = (0,255,0)
SPIN = (0,0,255)

if __name__ == "__main__":
    print(BOARD_VER)

import serial  # 导入串口通信模块
 
portx = "COM5"  # COM2口用来读数
# 设置并打开串口
ser = serial.Serial(portx, 115200)  
# 串口执行到这已经打开 再用open命令会报错
 
if ser.isOpen():  # 判断串口是否打开
    print("open success")
    ser.write("2101321\n".encode("ascii"))

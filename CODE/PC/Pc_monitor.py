import psutil
from pynvml import *
import time
import serial  # 导入串口通信模块
    
class PC_STAT():
    def __init__(self) -> None:
        nvmlInit()
    def get_cpu(self):
        time.sleep(0.05)
        self.cp_list = psutil.cpu_percent(percpu=True)
        self.cp_list.sort()
        self.cp_list = self.cp_list[::-1]
        self.cp_all = psutil.cpu_percent()
        return self.cp_all,self.cp_list
    def get_mem(self):
        self.mem = psutil.virtual_memory().percent
        return self.mem
    def get_gpu(self):
        self.gpu_handle = nvmlDeviceGetHandleByIndex(0)
        self.gpu_name = nvmlDeviceGetName(self.gpu_handle)
        self.gpu_mem_info = nvmlDeviceGetMemoryInfo(self.gpu_handle)
        self.gpu_mem_persent = round(100*self.gpu_mem_info.used/self.gpu_mem_info.free,2)
        self.gpu_temp = nvmlDeviceGetTemperature(self.gpu_handle,0)
        self.gpu_fan = nvmlDeviceGetFanSpeed(self.gpu_handle)
        return {'name':self.gpu_name,'mem':self.gpu_mem_persent,'tmp':self.gpu_temp,'fan':self.gpu_fan,'pwr':round(nvmlDeviceGetPowerUsage(self.gpu_handle)/1000.0,2)}

class PC_SERIAL_MONITOR():
    def __init__(self,port) -> None:
        self.portx = port  # COM2口用来读数
        # 设置并打开串口
        self.ser = serial.Serial(self.portx, 115200)
        self.pc = PC_STAT()
        self.led_buf = [[0,0,0]]*24
        self.led_bright = 20
        #print(self.led_buf)

    def test_monitor(self):
        self.ser.write("110L_STAT   MID MEM  SENTEN111 SENTENCE2ST#3     .\n".encode("ascii"))

        time.sleep(0.2)
        self.ser.write("0\n".encode("ascii"))

    def mem_on_seg(self):
        self.mem = self.pc.get_mem()
        self.mem_word = ("%.1f"%self.mem)
        if '.' in self.mem_word:
            self.point = len(self.mem_word) - self.mem_word.index('.')
        self.mem_word = self.mem_word.replace('.','')
        self.mem_word = '210'+'0'*(4-len(self.mem_word)) + self.mem_word + str(1+self.point) + '\n'
        print(self.mem,self.mem_word)
        self.ser.write(self.mem_word.encode("ascii"))

    def cpu_on_led(self,cpu_all,cpu_percore):# 2-12(true :1-11) for cpu monitor
        #self.change_led(1,[0,self.bright//2,self.bright//2])
        if cpu_all == 100:
            for i in range(1,12):
                self.change_led(i,[self.led_bright,0,0])
            self.send_led_mode0()
            return
        
        self.num_light = int(cpu_all*11//100+1)
        self.last_bright = cpu_all%10
        # clear MAX
        for i in range(1,12):
            self.change_led(i,[0,self.led_bright,1])
        
        for i in range(self.num_light-1):
            self.change_led(1+i,[self.led_bright,0,0])
        
        self.change_led(self.num_light,[int(0.3*self.led_bright*self.last_bright),int(0.2*self.led_bright*(10-self.last_bright)),0])
        self.send_led_mode0()
        print(self.num_light)

    def gpu_on_led(self,gpu_util,gpu_mem):# 24-20(true :23-19) for gpu_util || 18-14(true :17-13) for gpu_mem
        if gpu_util == 100:
            for i in range(23,18,-1):
                self.change_led(i,[self.led_bright,0,0])
            self.send_led_mode0()
        elif gpu_util != 100:
            for i in range(23,18,-1):
                self.change_led(i,[0,0,self.led_bright])
            self.send_led_mode0()


        if gpu_mem == 100:
            for i in range(17,12,-1):
                self.change_led(i,[self.led_bright,0,0])
            self.send_led_mode0()
            return
        
        self.num_light_mem = int(gpu_mem*5//100+1)
        self.last_bright_mem = gpu_mem%10
        # clear MAX
        for i in range(17,12,-1):
            self.change_led(i,[0,1,self.led_bright])
        
        for i in range(17,17-self.num_light_mem+1,-1):
            self.change_led(i,[self.led_bright,0,0])
        
        self.change_led(17-self.num_light_mem+1,[int(0.3*self.led_bright*self.last_bright_mem),0,int(0.2*self.led_bright*(10-self.last_bright_mem))])
        self.send_led_mode0()
        print('mem %d' %self.num_light_mem)

    def change_led(self,place,rgb_valu:list[3]):
        if place>=24:
            return
        self.led_buf[place] = rgb_valu
        #print(place)
        #print(self.led_buf)

    def send_led_mode0(self):
        self.led_chr = "310"
        for i in range(24):
            for j in range(3):
                self.num= hex(self.led_buf[i][j])[2:]
                if len(self.num)>=2:
                    self.num = self.num[-2:]
                else:
                    self.num = '0'*(2-len(self.num)) + self.num
                self.led_chr += self.num
        #print(self.led_chr)
        self.ser.write((self.led_chr+"\n").encode("ascii"))

if __name__ == "__main__":
    a = PC_STAT()
    print(a.get_cpu())
    print(a.get_mem())
    print(a.get_gpu())
    b = PC_SERIAL_MONITOR("COM5")
    #b.change_led(22,[100,0,0])
    b.send_led_mode0()
    """for i in range(24):
        b.change_led(i,[100,0,0])
        b.send_led_mode0()
        time.sleep(0.3)"""
    time.sleep(0.3)
    while True:
        x,_ = a.get_cpu()
        y = a.get_gpu()
        print(x)
        b.cpu_on_led(x,[0]*12)
        time.sleep(0.25)
        b.mem_on_seg()
        time.sleep(0.25)
        b.gpu_on_led(10,y['mem'])
        time.sleep(0.5)
    """while True:
        b.test_monitor()
        time.sleep(0.5)"""
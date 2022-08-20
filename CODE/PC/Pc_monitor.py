import psutil
from pynvml import *
import time
import serial  # 导入串口通信模块
import src.PyTherm.pytherm as pyTherm
import datetime

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
        self.gpu_mem_persent = round(100*self.gpu_mem_info.used/self.gpu_mem_info.total,2)
        self.gpu_temp = nvmlDeviceGetTemperature(self.gpu_handle,0)
        self.gpu_fan = nvmlDeviceGetFanSpeed(self.gpu_handle)
        return {'name':self.gpu_name,'mem':self.gpu_mem_persent,'tmp':self.gpu_temp,'fan':self.gpu_fan,'pwr':round(nvmlDeviceGetPowerUsage(self.gpu_handle)/1000.0,2),'max_pwr':round(nvmlDeviceGetPowerManagementLimit(self.gpu_handle)/1000.0,2)}

class PC_SERIAL_MONITOR():
    def __init__(self,port) -> None:
        self.pc = PC_STAT()
        self.dash = PC2Dash(port)
        self.led_bright = 20
        #print(self.led_buf)

    def test_monitor(self):
        self.dash.send_word("110L_STAT   MID MEM  SENTEN111 SENTENCE2ST#3     .")
        self.dash.change_oled(0,'Liu')
        self.dash.change_oled(1,'ZS\'s')
        self.dash.change_oled(2,'W0rk')
        self.dash.change_oled(3,'Hel10w!')
        self.dash.change_oled(4,'W0r1d!')
        self.dash.change_oled(5,'||||||||||',ifsend=True)   

    def mem_on_seg(self):
        self.mem = self.pc.get_mem()
        self.mem_word = ("%.1f"%self.mem)
        self.dash.change_seg(self.mem_word)

    def cpu_on_led(self,cpu_all,cpu_percore):# 2-12(true :1-11) for cpu monitor
        #self.change_led(1,[0,self.bright//2,self.bright//2])
        if cpu_all == 100:
            for i in range(1,12):
                self.dash.change_led(i,[self.led_bright,0,0])
            self.dash.send_led_mode0()
            return
        
        self.num_light = int(cpu_all*11//100+1)
        self.last_bright = cpu_all%10
        # clear MAX
        for i in range(1,12):
            self.dash.change_led(i,[0,self.led_bright,1])
        
        for i in range(self.num_light-1):
            self.dash.change_led(1+i,[self.led_bright,0,0])
        
        self.dash.change_led(self.num_light,[int(0.3*self.led_bright*self.last_bright),int(0.2*self.led_bright*(10-self.last_bright)),0])
        self.dash.send_led_mode0()
        #print(self.num_light)

    def gpu_on_led(self,gpu_util,gpu_mem):# 24-20(true :23-19) for gpu_util || 18-14(true :17-13) for gpu_mem
        self.dash.change_led(18,[5,5,5])
        if gpu_util >= 100:
            for i in range(18,23,1):
                self.dash.change_led(i,[self.led_bright,0,0])
            self.dash.send_led_mode0()
        elif gpu_util < 100:
            self.num_light_utl = int(gpu_util*5//100+1)
            self.last_bright_utl = gpu_util%10
            # clear MAX
            for i in range(19,24,1):
                self.dash.change_led(i,[0,1,self.led_bright])
            
            for i in range(19,19+self.num_light_utl-1):
                self.dash.change_led(i,[self.led_bright,0,0])
            
            self.dash.change_led(19+self.num_light_utl-1,[int(0.3*self.led_bright*self.last_bright_utl),0,int(0.2*self.led_bright*(10-self.last_bright_utl))])
            #print('gpu_util %.2f'%gpu_util)
            self.dash.send_led_mode0()

        time.sleep(0.12)
        if gpu_mem >= 100:
            for i in range(17,12,-1):
                self.dash.change_led(i,[self.led_bright,0,0])
            self.dash.send_led_mode0()
            return
        
        self.num_light_mem = int(gpu_mem*5//100+1)
        self.last_bright_mem = gpu_mem%10
        # clear MAX
        for i in range(17,12,-1):
            self.dash.change_led(i,[0,1,self.led_bright])
        
        for i in range(17,17-self.num_light_mem+1,-1):
            self.dash.change_led(i,[self.led_bright,0,0])
        
        self.dash.change_led(17-self.num_light_mem+1,[int(0.3*self.led_bright*self.last_bright_mem),0,int(0.2*self.led_bright*(10-self.last_bright_mem))])
        self.dash.send_led_mode0()
        #print('mem %d' %self.num_light_mem)
    
    def temp_on_screen(self,cpu_tmp,gpu_tmp):
        self.dash.change_oled(3,"CPU:"+" "*(4-len(str(cpu_tmp)[0:2]))+str(cpu_tmp)[0:2]+" C",iflcear=True)
        #now_time = datetime.datetime.now()
        self.dash.change_oled(5,"Time:" + time.strftime("%H", time.localtime()) + ":" + time.strftime("%M", time.localtime()))
        self.dash.change_oled(4,"GPU:"+" "*(4-len(str(gpu_tmp)))+str(gpu_tmp)+" C",ifsend=True)
        pass

    """def change_led(self,place,rgb_valu:list[3]):
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
        self.ser.write((self.led_chr+"\n").encode("ascii"))"""

class PC2Dash():
    def __init__(self,port='COM5') -> None:
        self.portx = port  # COM2口用来读数
        # 设置并打开串口
        self.ser = serial.Serial(self.portx, 115200)
        self.led_buf = [[0,0,0]]*24
        self.oled_buf = ['1','1','0']+[" "]*48
        #self.led_bright = 20

    def change_seg(self,seg_word):
        if '.' in seg_word:
            self.point = len(seg_word) - seg_word.index('.')
        seg_word = seg_word.replace('.','')
        seg_word = '210'+'0'*(4-len(seg_word)) + seg_word + str(1+self.point)
        #print(seg_word)
        self.send_word(seg_word)
        pass

    def send_word(self,word):
        self.ser.write((word+"\n").encode("ascii"))
        time.sleep(0.2)
        print('send word:'+word)

    def change_oled(self,pos,word,mode=0,iflcear=False,ifsend=False):
        if iflcear:
            self.oled_buf = ['1','1','0']+[" "]*48
        if mode == 0:
            if pos<3:#banner
                j = 0
                for i in word:
                    self.oled_buf[pos*6+3+j] = i
                    j += 1
                    if j >=6:
                        break
            elif pos<6:
                j = 0
                for i in word:
                    self.oled_buf[(pos-3)*10+21+j] = i
                    j += 1
                    if j >=10:
                        break
        
        if ifsend:
            self.send_word("".join(self.oled_buf))
            #time.sleep(0.25)
            
    def change_led(self,place,rgb_valu:list[3]):
        if place>=24:
            return
        self.led_buf[place] = rgb_valu

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
        print("send led:%s" %self.led_chr)



if __name__ == "__main__":
    a = PC_STAT()
    print(a.get_cpu())
    print(a.get_mem())
    print(a.get_gpu())
    b = PC_SERIAL_MONITOR("COM5")
    #b.change_led(22,[100,0,0])
    b.dash.send_led_mode0()
    b.test_monitor()
    """for i in range(24):
        b.change_led(i,[100,0,0])
        b.send_led_mode0()
        time.sleep(0.3)"""
    time.sleep(0.3)
    i = 0
    while True:
        x,_ = a.get_cpu()
        y = a.get_gpu()
        #print(x)
        b.cpu_on_led(x,[0]*12)
        time.sleep(0.25)
        b.mem_on_seg()
        time.sleep(0.12)
        b.gpu_on_led(100*y['pwr']/y['max_pwr'], y['mem']) #
        time.sleep(0.12)
        if i%10 == 0:
            b.temp_on_screen(pyTherm.get_cpu(),y['tmp'])
        i += 1
    """while True:
        b.test_monitor()
        time.sleep(0.5)"""
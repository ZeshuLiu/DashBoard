from pynvml import *
nvmlInit()     #初始化
print("Driver: "+nvmlSystemGetDriverVersion())  #显示驱动信息
#>>> Driver: 384.xxx

#查看设备
deviceCount = nvmlDeviceGetCount()
for i in range(deviceCount):
    handle = nvmlDeviceGetHandleByIndex(i)
    print("GPU", i, ":", nvmlDeviceGetName(handle))
    print(handle)
    handle = nvmlDeviceGetHandleByIndex(0)
    info = nvmlDeviceGetMemoryInfo(handle)
    print(info)
    print("Memory Total: ",info.total/(1024.0**3))
    print("Memory Free: ",info.free/(1024.0**3))
    print("Memory Used: ",info.used/(1024.0**3))
    print("Memory Persent: %.2f%%"%(100*info.used/info.free))
    print("Temperature is %d C"%nvmlDeviceGetTemperature(handle,0))
    print("Fan speed is ",nvmlDeviceGetFanSpeed(handle))
    print("Power usage %.2f W" %(nvmlDeviceGetPowerUsage(handle)/1000.0))
    print("Power max %.2f W" %(nvmlDeviceGetPowerManagementLimit(handle)/1000))
    print(nvmlDeviceGetPerformanceState(handle))
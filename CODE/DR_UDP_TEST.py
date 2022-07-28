import socket
import time
import struct

from numpy import in1d

global fmt
fmt = '<' + '61' + 'f'  # define structure of packed data

global s
s = struct.Struct(fmt)  # declare structure

def main():
    # 1.创建一个udp套接字
    

    # 2.绑定本地的相关信息，如果一个网络程序不绑定，则系统会随机分配
    # 30000  表示本地的端口 ip一般不用写
    print("Udp On!")
    
    # 3. 等待接收对方发送的数据
     
    # 1024表示本次接收的最大字节数

    # 6. 显示对方发送的数据
    # 接收到的数据recv_data是一个元组
    # 第1个元素是对方发送的数据
    # 第2个元素是对方的ip和端口
    while True:
        udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        local_addr = ("127.0.0.1", 50777)
        udp_socket.bind(local_addr)
        recv_data = udp_socket.recvfrom(1024) 
        by = recv_data[0]
        #unpacked_data = s.unpack(by) 

        print(str(struct.unpack('f', by[132:132+4])[0]))
        print(recv_data[1])
        time.sleep(2)
    # 3.关闭套接字
    udp_socket.close()


if __name__ == "__main__":
    main()
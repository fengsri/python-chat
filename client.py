import os, sys
import threading
from socket import *
from select import select

def main():
    'main 主函数'
    client = socket(AF_INET, SOCK_STREAM)  # 建立TCP套接字
    if login(client):
        t_recv = threading.Thread(target=recv, args=(client,))
        t_send = threading.Thread(target=send_msg, args=(client,))
        t_recv.start()
        t_send.start()

def send_msg(client):
    while True:
        send_data = input("请输入要发送的数据：")
        send_data = username + ":" +send_data
        client.send(send_data.encode("utf-8"))

def recv(client):
    # 使用select模块的select方法实现IO多路复用监听传输
    rlist = [client]
    wlist = []
    xlist = []

    while True:
        rs, ws, xs = select(rlist, wlist, xlist)
        for r in rs:
            if r is client:
                # 接受服务器发来的消息
                data = client.recv(1024)
                if data.decode() == '\n':
                    # 如果消息为回车，聊天室关闭
                    client.close()
                    os._exit(0)
                else:
                    # 打印接收到的信息
                    print(data.decode(), end='')

def login(client):
    '登录函数 login'
    curuser = input('输入名称>')
    global username
    username = curuser
    ADDR = '127.0.0.1', 5555
    client.connect(ADDR)  # 连接到服务器地址
    data = curuser + ': ' + "进入房间"
    client.send(data.encode())
    return True

if __name__ == '__main__':
    main()

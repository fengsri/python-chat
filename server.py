from socket import *
from select import select

def main():
    'main 主函数'
    server = socket(AF_INET, SOCK_STREAM)  # 建立TCP套接字
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # 设置端口可立即重用
    ADDR = '127.0.0.1', 5555
    server.bind(ADDR)  # 绑定地址
    server.listen()  # 监听
    # 接收函数
    accept(server)


def accept(server):
    'accept 服务器接受函数'
    # 使用select模块的select方法实现IO多路复用监听传输
    rlist = [server]
    wlist = []
    xlist = []

    while True:
        rs, ws, xs = select(rlist, wlist, xlist)
        for r in rs:
            # 服务器接受客户端连接
            if r is server:
                try:
                    conn, addr = server.accept()
                    welcome(conn)
                    # 将客户端套接字添加到rlist中以监听
                    rlist.append(conn)
                    print("链接从：", addr)
                except:
                    pass

            else: # 服务器接受客户端的消息并转发给所有客户端
                try:
                    data = r.recv(1024)
                    # 转发信息给其他客户端
                    data = b'\n' + data + b'\n'
                    print(data.decode(), end='')
                    for c in rlist[1:]:
                        if c is not r:
                            c.send(data)
                except:
                    rlist.remove(r)

def welcome(client):
    client.send(b'Welcome! \n')
    return True

if __name__ == '__main__':
    # 主函数
    main()

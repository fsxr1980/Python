"""
    Server of Chatroom
    env:python 3.8
"""
from socket import *
import os,sys

host_ser = ('192.168.96.130',6666)
# dict_name = {}
list_name = []

# sign in function --approve client enter chatroom
def do_login(sock_ser,name,addr):
    if (name,addr) in list_name:
        sock_ser.sendto(b'the name is exist',addr)
        return
    sock_ser.sendto(b'ok',addr)
    # Notify others
    msg ='welcome %s enter chat room'%name
    for item in list_name:
        sock_ser.sendto(msg.encode(),item[1])
    # Join users
    list_name.append((name,addr))

# chating function
def do_chating(sock_ser,msg,text):
    msg = '/n%s:%s'%(msg,text)
    for name,addr in list_name:
        if name != msg:
            sock_ser.sendto(msg.encode(), addr)

# sign out function
def do_quit(sock_ser,name):
    msg = '%s is quit chat room'%name
    for name,addr in list_name:
        if name != name:
            sock_ser.sendto(msg.encode(),addr)
        else:
            sock_ser.sendto(b'EXIT', addr)

        list_name.remove((name,addr))


def do_request(sock_ser):
    """
    Processing request
    :param sock_ser: socket
    :return:
    """
    while True:
        data, addr = sock_ser.recvfrom(1024)
        req_msg = data.decode().split(' ')
        # sign in
        if req_msg[0] == 'L':
            do_login(sock_ser,req_msg[1],addr)
        elif req_msg[0] == 'C':
            if (req_msg[1],addr) not in list_name:
                sock_ser.sendto(b'EXIT',addr)
                continue
            text = ' '.join(req_msg[2:])
            do_chating(sock_ser,req_msg[1],text)
        elif req_msg[0] == 'Q':
            if (req_msg[1],addr) not in list_name:
                sock_ser.sendto(b'EXIT',addr)
                continue
            do_quit(sock_ser,req_msg[1])

def main():
    """
    create connection
    :return:
    """
    sock_ser = socket(AF_INET,SOCK_DGRAM)
    sock_ser.bind(host_ser)

    pid = os.fork()
    if pid < 0:
        return
    #send admin massage
    elif pid == 0:
        while True:
            msg = input('/nadmin massage:')
            msg = 'C admin massage ' + msg
            sock_ser.sendto(msg.encode(),host_ser)
    else:
        # request deal
        do_request(sock_ser)


# chating function




if __name__ == "__main__":
    main()

"""
    the client of chatroom
    env: python 3.8
"""

from socket import *
import os,sys
from time import sleep

HOST_SER =('192.168.96.130',6666)

# recv massage
def msg_recv(sock_cli):
    while True:
        msg_recv, addr = sock_cli.recvfrom(1024)
        if msg_recv.decode() == "EXIT":
            sys.exit()
        print(msg_recv.decode())

#send massage
def msg_send(sock_cli,name):
    while True:
        try:
            text = input('please input your massage:')
        except KeyboardInterrupt:
            text = 'quit'
        if text == 'quit':
            msg_send = 'Q ' + name
            sock_cli.sendto(msg_send.encode(), HOST_SER)
            sys.exit('quit chat room.')
        msg_send = 'C %s %s'%(name,text)
        sock_cli.sendto(msg_send.encode(), HOST_SER)
        sleep(0.5)
# sign out
def c_quit(sock_cli,cha_):
    sock_cli.sendto(cha_.encode(), HOST_SER)
    sleep(2)

# create connetion
def main():
    sock_cli = socket(AF_INET,SOCK_DGRAM)
    while True:
        name = input('please enter your name:')
        msg = 'L ' + name
        sock_cli.sendto(msg.encode(),HOST_SER)
        # wait reponse
        msg,addr = sock_cli.recvfrom(1024)
        if msg.decode() == 'ok':
            print('You have entered the chat room')
            break
        else:
            print('Name used,please enter a new name.')


    pid = os.fork()
    if pid < 0:
        sys.exit('Error')
    elif pid == 0:
        msg_send(sock_cli,name)
    else:
        msg_recv(sock_cli)









if __name__ == "__main__":
    main()



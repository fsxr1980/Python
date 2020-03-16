"""
    ftp file server concurrency
"""

from socket import *
from threading import Thread
import os
from time import sleep

HOST = "0.0.0.0"
PORT = 8866
ADDR = (HOST, PORT)
Lib_file = "/home/lgb/FTP/"

class FtpServer:
    def __init__(self,sock_n,PATH):
        self.sock_n = sock_n
        self.PATH = PATH

    def find_(self):
        files = os.listdir(self.PATH)
        if not files:
            self.sock_n.send(b'No files.')
        else:
            self.sock_n.send(b'ok')
            sleep(0.1)
        fs = ''
        for file in files:
            if file[0] != '.' and os.path.isfile(self.PATH + file):
                fs += file + "\n"
        sleep(0.1)
        self.sock_n.send(fs.encode())

    def download(self,file):
        print(file)
        if file not in os.listdir(self.PATH):
            self.sock_n.send(b"wrong")
        else:
            fl = open(self.PATH + file,'rb')
            while True:
                data = fl.read(1024)
                if not data:
                    self.sock_n.send(b'##')
                    break
                self.sock_n.send(data)
            print("download finished.")
            fl.close()


    def upload(self,file):
        if file in os.listdir(self.PATH):
            self.sock_n.send(b'wrong')
        else:
            self.sock_n.send(b'ok')
            fl = open(self.PATH + file,'wb')
            while True:
                data = self.sock_n.recv(1024)
                if not data or data.decode() == 'over':
                    print('##')
                    break
                else:
                    fl.write(data)
            self.sock_n.send(b'upload ok')
            print('a')
            fl.close()


def handle(sock_n):
    sock_n.send(b"Connect succesful. ")

    cls = sock_n.recv(1024).decode()
    PATH = Lib_file + cls + '/'
    ftp = FtpServer(sock_n,PATH)
    while True:
        data = sock_n.recv(1024).decode()
        if not data or data[0] == 'q':
            return
        elif data[0] == 'l':
            ftp.find_()
        elif data[0] == "G":
            ftp.download(data.split()[-1])
        elif data[0] == "P":
            ftp.upload(data.split()[-1])

# Network building
def main():
    sock_s = socket(AF_INET,SOCK_STREAM)
    sock_s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)

    sock_s.bind(ADDR)
    sock_s.listen(5)
    print("Listen the port 8866...")
    while True:
        try:
            sock_n,addr = sock_s.accept()
        except KeyboardInterrupt:
            return
        except Exception as e:
            print("Connect Failed,Bye.")
            continue
        print("connect client:",addr)
        t_s = Thread(target=handle,args=(sock_n,))
        t_s.setDaemon(True)
        t_s.start()

if __name__ == "__main__":
    main()
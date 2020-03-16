from socket import socket
import sys
from time import sleep

class FtpClient:
    def __init__(self,sock_c):
        self.sock_c = sock_c

    def do_list(self):
        self.sock_c.send(b'list')
        data = self.sock_c.recv(128).decode()
        if data == "ok":
             data = self.sock_c.recv(1024)
             print(data.decode())
        else:
            print(data)

    def get_file(self,file):
        self.sock_c.send(('G ' + file).encode())
        fl = open(file,'wb')
        while True:
            data = self.sock_c.recv(1024)
            if data.decode() == 'wrong':
                print("File isn't exist.")
                break
            else:
                if data.decode() == '##':
                    return
                fl.write(data)
        fl.close()

    def put_file(self,file):
        fl = open(file,'rb')
        file = file.split("/")[-1]
        self.sock_c.send(('P '+ file).encode())
        data = self.sock_c.recv(1024).decode()
        if data == 'wrong':
            print('file is exsit.')

        elif data == "ok":
            while True:
                data = fl.read()
                if not data:
                    sleep(0.1)
                    self.sock_c.send(b'over')
                    break
                else:
                    self.sock_c.send(data)

            data = self.sock_c.recv(1024).decode()
            print(data)
        fl.close()

    def do_quit(self):
        self.sock_c.send(b'Q')
        self.sock_c.close()
        sys.exit("bye")

def request(sock_c):
    request_c = FtpClient(sock_c)
    while True:
        print( """\n Command options:
                     *****list****** 
                     **upload file**
                     *download file*
                     *****quit*****      
        """)

        cmd = input("input the request:")
        if cmd.strip() == 'list':
            request_c.do_list()
        elif cmd.strip().split()[0] == 'download':
            request_c.get_file(cmd.strip().split()[-1])
        elif cmd.strip().split()[0] == 'upload':
            request_c.put_file(cmd.strip().split()[-1])
        elif cmd.strip() == 'quit':
            request_c.do_quit()



def main():
    ADDR = ('127.0.0.1',8866)
    sock_c = socket()
    try:
        sock_c.connect(ADDR)
    except Exception as e:
        print("connect failed.")
        return
    else:
        print(sock_c.recv(1024).decode())

        print("""****************************
                    Data    File   Image
                *****************************
        """)
        cls = input('please input file class:').strip()
        if cls not in ['Data','File','Image']:
            print("Sorry, input wrong.")
        else:
            sock_c.send(cls.encode())
            request(sock_c)

if __name__ == "__main__":
    main()
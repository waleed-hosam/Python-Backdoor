from os import path
from datetime import datetime
class Recv:
    def __init__(self, conn, filename, size):
        file = open(f"../download/{filename}", "wb")
        file_bytes = b""
        done = False
        while not done:
            data = conn.recv(size)
            if data[-5:] == b"<END>":
                data.replace(b"<END>", b"")
                file_bytes += data.replace(b"<END>", b"")
                done = True
                break
            else:
                file_bytes += data
        file.write(file_bytes)
        file.close()
        print("file transfer complete")


class Send:
    def __init__(self, conn, file_name: str):
        file = open(file_name, 'rb')
        data = file.read()
        conn.sendall(data)
        conn.send(b"<END>")
        file.close()
        print("transfer complete")


class Recv_ScreenShot:
    def __init__(self, conn, size):
        name = "screenshot-{}.png".format(str(datetime.now()).replace(":", "."))
        screenshot_path = "..\\screenshots\\{}".format(name)
        file = open(screenshot_path, "wb")
        file_bytes = b""
        done = False
        while not done:
            data = conn.recv(size)
            if data[-5:] == b"<END>":
                data.replace(b"<END>", b"")
                file_bytes += data.replace(b"<END>", b"")
                done = True
                break
            else:
                file_bytes += data
        file.write(file_bytes)
        file.close()
        print("screenshot taken")

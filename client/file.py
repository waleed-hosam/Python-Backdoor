from os import remove
from pyautogui import screenshot
class Send:
    def __init__(self, conn, file_name: str):
        file = open(file_name, "rb")
        data = file.read()
        conn.sendall(data)
        conn.send(b"<END>")
        file.close()
        print("transfer complete")


class Recv:
    def __init__(self, conn, filename, size):
        file = open(f"{filename}", "wb")
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


class ScreenShot:
    def __init__(self, conn):
        Thescreenshot = screenshot()
        file_name = "my_ready_screenshot.png"
        Thescreenshot.save(file_name)
        file = open(file_name, "rb")
        data = file.read()
        conn.sendall(data)
        conn.send(b"<END>")
        file.close()
        print("screenshot taken")
        remove("my_ready_screenshot.png")
        print("removed")


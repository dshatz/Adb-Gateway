import sys
import threading
import queue
from time import sleep

import paramiko
from adbutils import AdbClient
from paramiko import SSHClient
from sshtunnel import SSHTunnelForwarder, open_tunnel

from rforward import reverse_forward_tunnel
import tkinter as tk

q = queue.Queue()


def worker():
    adb = AdbClient(host="127.0.0.1", port=5037)
    while True:
        try:
            for info in adb.list():
                print(info.serial, info.state)
            q.put("adbok")
            try:
                q.put("connected")
                reverse_forward_tunnel(
                    5037, "localhost", 5037, ssh()
                )
            except Exception as e:
                q.put("ssherror:SSH tunnel error " + str(e))

        except ConnectionRefusedError:
            q.put("adbnotok")
        sleep(1000)

def ssh():
    ssh: SSHClient = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
        hostname='158.179.200.162',
        port=2222,
        username="headless",
        password="Confero123!"
    )
    return ssh.get_transport()


def worker2():
    try:
        q.put("connected2")
        reverse_forward_tunnel(
            27183, "localhost", 27183, ssh()
        )
    except Exception as e:
        q.put("ssherror:SSH tunnel error(2) " + str(e))

class App():
    def __init__(self, root):
        self.adberror = tk.Label(text="No ADB daemon found", fg="#f00")
        self.adbOk = tk.Label(text="ADB found")
        self.ssherror = tk.Label(text="")
        self.connected = tk.Label(text="Connected", fg="#008000")
        self.connected2 = tk.Label(text="Connected (2)", fg="#008000")
        self.root = root

    def after_callback(self):
        try:
            message = q.get(block=False)
        except queue.Empty:
            # let's try again later
            self.root.after(100, self.after_callback)
            return

        print('after_callback got', message)
        if message is not None:
            # we're not done yet, let's do something with the message and
            # come back later
            if message == "adbnotok":
                self.adberror.pack()
            if message == "adbok":
                self.adbOk.pack()
                self.adberror.destroy()
            if message.startswith("ssherror:"):
                self.ssherror = tk.Label(text=message[9:], fg="#f00")
                self.ssherror.pack()
            if message == "connected":
                self.connected.pack()
            if message == "connected2":
                self.connected2.pack()
            self.root.after(100, self.after_callback)


def main():
    window = tk.Tk()
    window.title("ADB Gateway")
    window.geometry("400x300")

    thread = threading.Thread(target=worker)
    thread.start()

    thread2 = threading.Thread(target=worker2)
    thread2.start()
    app = App(window)
    window.after(100, app.after_callback)
    window.mainloop()





if __name__ == "__main__":
    main()

import multiprocessing
import os
import queue
import tkinter as tk
from tkinter import END, messagebox
from tkinter.ttk import Notebook

from adbgateway.access import WorkerAccess
from adbgateway.share import WorkerShare
from adbgateway.config import Config, ConfigCreated


class App:
    def __init__(self, root):
        try:
            self.config = Config()
        except ConfigCreated as e:
            messagebox.showwarning(title="Error", message="Config file created, please edit adbgateway.cfg")
            raise e

        self.root = root
        self.tabs = Notebook(self.root)
        self.tabShare = tk.Frame(self.tabs)
        self.tabAccess = tk.Frame(self.tabs)
        self.tabs.add(self.tabShare, text="Share device")
        self.tabs.add(self.tabAccess, text="Access device")
        self.tabs.pack(expand=1, fill="both")

        self.logShare = tk.Text(self.tabShare)
        self.logAccess = tk.Text(self.tabAccess)
        self.launchScrcpy = tk.Button(self.tabAccess, command=self.scrcpy, text="scrcpy")
        self.launchScrcpy.pack()
        self.logShare.pack()
        self.logAccess.pack()

        self.workerShare = WorkerShare(self.config)
        self.workerAccess = WorkerAccess(self.config)

    def scrcpy(self):
        os.system(
            f"ANDROID_ADB_SERVER_PORT={self.config.access_adb_port} scrcpy"
            f" --tunnel-port={self.config.access_scrcpy_port}"
            f" -b 1M --max-fps=15 --max-size=1024"
        )

    def after_callback(self):
        selected = self.tabs.index("current")
        if selected == 0 and not self.workerShare.running:
            # Share device selected.
            self.workerShare = WorkerShare(self.config)
            self.workerShare.start()
            if self.workerAccess.running:
                self.workerAccess.stop()
            self.logAccess.delete("1.0", END)
        elif selected == 1 and not self.workerAccess.running:
            # Access device selected.
            self.workerAccess = WorkerAccess(self.config)
            self.workerAccess.start()
            if self.workerShare.running:
                self.workerShare.stop()
            self.logShare.delete("1.0", END)

        try:
            if selected == 0 and self.workerShare.running:
                message = self.workerShare.q.get(block=False)
            elif selected == 1 and self.workerAccess.running:
                message = self.workerAccess.q.get(block=False)
            else:
                message = ""
            if message != "":
                print(f"Message from page {selected}: {message}")
                self.process_message(selected, message)
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.after_callback)

    def process_message(self, page, msg):
        if page == 0:
            self.logShare.insert(END, msg + "\n")
            self.logShare.pack()
        elif page == 1:
            if msg == "show_scrcpy_button":

                pass
            else:
                self.logAccess.insert(END, msg + "\n")
                self.logShare.pack()

    def stop(self):
        if self.workerShare is not None:
            self.workerShare.stop()
        if self.workerAccess is not None:
            self.workerAccess.stop()


def main():
    window = tk.Tk()
    window.title("ADB Gateway")
    window.geometry("400x300")

    app = App(window)

    window.after(100, app.after_callback)
    window.mainloop()
    app.stop()


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()

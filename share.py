import os
import subprocess
from abc import ABC
from multiprocessing import Process
from queue import Queue
from time import sleep

import adbutils
from adbutils import adb_path, AdbConnection

from config import Config
from rforward import reverse_forward_tunnel
from ssh import ssh
from worker import Worker


def worker_share_adb(worker: Worker):
    print("worker_share_adb")
    try:
        # Start adb server at port 5040
        p = subprocess.run([adb_path(), "devices"], env={"ANDROID_ADB_SERVER_PORT": "5037"}, capture_output=True, text=True)
        worker.send_message(p.stdout)

        # Wait for at least one device
        adb = adbutils.AdbClient("127.0.0.1", 5037)
        while len(adb.device_list()) == 0:
            worker.send_message("No devices found, waiting 10s...")
            sleep(10)

        worker.send_message("Devices: " + ", ".join(map(lambda x: x.serial, adb.device_list())))
        worker.send_message(f"ADB tunnel localhost:5037 -> 5038...")
        reverse_forward_tunnel(
            5038, "localhost", 5037, ssh(worker.config)
        )
    except Exception as e:
        print(e)
        worker.send_message(f"Could not create ADB tunnel: {e}")


def worker_share_scrcpy(worker: Worker):
    print("worker_share_scrcpy")
    try:
        worker.send_message(f"Scrcpy tunnel localhost:{worker.config.share_scrcpy_port} -> 27184...")
        reverse_forward_tunnel(
            27184, "localhost", int(worker.config.share_scrcpy_port), ssh(worker.config)
        )
    except Exception as e:
        print(e)
        worker.send_message(f"Could not create Scrcpy tunnel: {e}")


class WorkerShare(Worker, ABC):
    def create_processes(self):
        self.processes = [
            Process(target=worker_share_adb, args=[self]),
            Process(target=worker_share_scrcpy, args=[self])
        ]
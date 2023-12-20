from abc import ABC
from multiprocessing import Process
from time import sleep

from sshtunnel import SSHTunnelForwarder

from adbgateway.tools import kill_adb_server
from adbgateway.worker import Worker


def worker_access_adb(worker: Worker):
    print("worker_share_adb")
    try:
        # Kill adb that is running on port that we need to bind to.
        kill_adb_server(worker.config.access_adb_port)

        worker.send_message(f"Connecting to remote adb 5038 -> localhost:{worker.config.access_adb_port}")
        server = SSHTunnelForwarder(
            ssh_address_or_host=worker.config.ssh_host,
            ssh_port=worker.config.ssh_port,
            ssh_username=worker.config.ssh_user,
            ssh_password=worker.config.ssh_pass,
            local_bind_address=('127.0.0.1', int(worker.config.access_adb_port)),
            remote_bind_address=('127.0.0.1', 5038)
        )
        server.start()
        while True:
            sleep(1)
    except Exception as e:
        print(e)
        worker.send_message(f"Could not create ADB tunnel: {e}")


def worker_access_scrcpy(worker: Worker):
    print("worker_share_scrcpy")
    try:
        worker.send_message(f"Connecting to remote scrcpy 27184 -> localhost:{worker.config.access_scrcpy_port}...")
        server = SSHTunnelForwarder(
            ssh_address_or_host=worker.config.ssh_host,
            ssh_port=worker.config.ssh_port,
            ssh_username=worker.config.ssh_user,
            ssh_password=worker.config.ssh_pass,
            local_bind_address=('127.0.0.1', int(worker.config.access_scrcpy_port)),
            remote_bind_address=('127.0.0.1', 27184)
        )
        server.start()
        worker.send_message(f"You can now run ANDROID_ADB_SERVER_PORT={worker.config.access_adb_port} scrcpy --tunnel-port={worker.config.access_scrcpy_port}")
        worker.send_message("show_scrcpy_button")
        while True:
            sleep(1)
    except Exception as e:
        print(e)
        worker.send_message(f"Could not create Scrcpy tunnel: {e}")


class WorkerAccess(Worker, ABC):
    def create_processes(self):
        self.processes = [
            Process(target=worker_access_adb, args=[self]),
            Process(target=worker_access_scrcpy, args=[self])
        ]
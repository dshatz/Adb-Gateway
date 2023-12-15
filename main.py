import sys
from os.path import isfile

import os.path
from time import sleep

import paramiko
from adbutils import AdbClient
from sshtunnel import SSHTunnelForwarder, open_tunnel

from rforward import reverse_forward_tunnel


def main():
    adb = AdbClient(host="127.0.0.1", port=5037)
    for info in adb.list():
        print(info.serial, info.state)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
        hostname='158.179.200.162',
        port=22,
        username="adb-tunnel",
        password=""
    )
    transport = ssh.get_transport()
    try:
        reverse_forward_tunnel(
            5037, "localhost", 5037, transport
        )
    except KeyboardInterrupt:
        print("C-c: Port forwarding stopped.")
        sys.exit(0)





if __name__ == "__main__":
    main()

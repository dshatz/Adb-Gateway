import paramiko
from paramiko.client import SSHClient

from adbgateway.config import Config


def ssh(config: Config):
    ssh: SSHClient = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
        hostname=config.ssh_host,
        port=int(config.ssh_port),
        username=config.ssh_user,
        password=config.ssh_pass
    )
    return ssh.get_transport()
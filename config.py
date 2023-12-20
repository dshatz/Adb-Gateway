from os import getenv
import configparser
from os.path import isfile
from shutil import copyfile


class ConfigCreated(Exception):
    pass


class Config:
    def __init__(self):
        config = configparser.ConfigParser()
        if not isfile("adbgateway.cfg"):
            copyfile("default.cfg", "adbgateway.cfg")
            raise ConfigCreated()
        config.read('adbgateway.cfg')
        ssh = config['SSH']
        self.ssh_host = ssh['HOST']
        self.ssh_port = ssh['PORT']
        self.ssh_user = ssh['USER']
        self.ssh_pass = ssh['PASSWORD']

        share = config['SHARE']
        self.share_scrcpy_port = share['SCRCPY_PORT']

        access = config['ACCESS']
        self.access_adb_port = access['ADB_PORT']
        self.access_scrcpy_port = access['SCRCPY_PORT']

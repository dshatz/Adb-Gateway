from os import getenv
import configparser
from os.path import isfile
from pkgutil import get_data


class ConfigCreated(Exception):
    pass


def def_config():
    return get_data("adbgateway", "default.cfg").decode('ascii')


class Config:
    def __init__(self):
        config = configparser.ConfigParser()
        if not isfile("adbgateway.cfg"):
            with open("adbgateway.cfg", "w") as f:
                f.write(def_config())
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

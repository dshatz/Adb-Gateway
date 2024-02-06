# ADB over SSH gateway - share Android devices connected to your computer through ADB with any other computer.

## Requirements
 - Linux or Windows
 - adb
 - scrcpy (optional)

## Running
You can download a packaged standalone executable from [GitHub releases](https://github.com/dshatz/Adb-Gateway/releases).

On the first run, AdbGateway will create a sample config file and close. 
You need to fill it in with your connection details before proceeding.

### Config
`adbgateway.cfg`
```properties
[SSH]
# Connection details to your SSH server.
HOST=your_ssh_server_ip
PORT=22
USER=your_ssh_username
PASSWORD=""

[SHARE]
# In sharing mode, these ports will be tunneled to the ssh server above.
# Defaults should work fine in most cases.
# Local scrpy port, default 27183.
SCRCPY_PORT=27183

[ACCESS]
# In access mode, these ports on your local machine will be connected to the ssh server and receive all traffic from the computer running in 'Share' mode.

# Local adb server port on which the remote adb server will be accessible, default 5037.
# If using non-default port, run adb as follows: ANDROID_ADB_SERVER_PORT=<ADB_PORT> adb devices
ADB_PORT=5037

# Local scrcpy port on which the remote scrcpy will be accessible.
# To force scrcpy to use this port, run as follows:
# ANDROID_ADB_SERVER_PORT=<ADB_PORT> scrcpy --tunnel-port=<SCRCPY_PORT>
# Make sure to also specify max bitrate and resolution for better performance.
SCRCPY_PORT=27183
```

## Operating modes
![window.png](readme%2Fwindow.png)

### Share device
Let's say you have an Android device on which some bug is easily reproducible.
At the same time, the developer who is supposed to fix this bug can not reproduce it on his devices.

### Access device
Let's say you are that developer who can't reproduce a bug. 
Ask your QA team to run AdbGateway in 'Share' mode to access their device logs and scrcpy.

![scheme.png](readme%2Fscheme.png)


## How to use
*Please note that both sides should be connecting to the same SSH server.*
### Share local ADB devices
1. Fill in the SSH server details in the configuration. You can leave the rest as is.
2. Launch ADB Gateway and make sure you are in the **Share device** tab.
3. Connect your Android to your computer through adb (USB or wireless).

### Access remote ADB devices
1. Fill in the SSH server details in the configuration. You can leave the rest as is.
2. Launch ADB Gateway and switch to **Access device** tab.

#### Run adb
```bash
ANDROID_ADB_SERVER_PORT=<ADB_PORT> adb ...
```

#### Run scrcpy
```bash
ANDROID_ADB_SERVER_PORT=<ADB_PORT> scrcpy --tunnel-port=<SCRCPY_PORT>
```
Consider adding quality restrictions, see [ScrCpy documentation on the topic](https://github.com/Genymobile/scrcpy/blob/master/doc/video.md).
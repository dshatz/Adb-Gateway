from adbutils import AdbClient


def kill_adb_server(port):
    try:
        AdbClient(host="127.0.0.1", port=int(port)).server_kill()
    except:
        print(f"Could not kill adb:{port}")
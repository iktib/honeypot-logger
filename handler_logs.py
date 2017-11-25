from flask import Flask
from flask_script import Manager, Server
from flask_cache import Cache
import os, base64, json, subprocess
import re
import requests
app = Flask(__name__)
manager = Manager(app)

Main_Server = ""  # Logs are sent to this server
Host_logger = 'localhost'
Port_logger = 5000


@app.route('/get_logs', methods=['GET'])
def get_logs():
    if os.path.getsize("access.log") == 0:
        log_data = {"status": False, 'data': []}
    else:
        new_logs_access = open("access.log")
        storage_log_access = open("access_save.log", "a")
        addrs = []
        log_data = {"status": True, "data": []}
        for line in new_logs_access:
            storage_log_access.write(line)
            log_data["data"].append(base64.b64encode(line))
            addrs.append(re.findall(r'([0-9] +\.[0-9] +\.[0-9] +\.[0-9] +):([0-9]+)', line)[0])
        alert(addrs)
        new_logs_access.close()
        os.remove("access.log")

        open("access.log", 'a').close()
        storage_log_access.close()

    log_data = json.dumps(log_data)
    return log_data


@app.route('/status', methods=['GET'])
def status():
    status_honeypot = subprocess.check_output("ps aux | grep bap.py | grep -v \"grep\" || true",
                                              shell=True, stderr=subprocess.STDOUT)
    if status_honeypot:
        return "True"
    else:
        return "False"


def alert(addr):
    unique_addr = []
    for i in addr:
        if i not in unique_ddr:
            unique_addr.append(i)
    for ip_port in unique_addr:
        r = requests.post(Main_Server, data={'alert': ip_port})


if __name__ == '__main__':
    manager.add_command("runserver", Server(use_debugger=True, host=Host_logger, port=Port_logger))
    manager.run()
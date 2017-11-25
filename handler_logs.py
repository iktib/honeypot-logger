from flask import Flask
from flask_script import Manager, Server
from flask_cache import Cache
import os, base64, json, subprocess

app = Flask(__name__)
manager = Manager(app)


@app.route('/get_logs', methods=['GET'])
def get_logs():
    if os.path.getsize("access.log") == 0:
        log_data = {"status": False, 'data': []}
    else:
        new_logs_access = open("access.log")
        storage_log_access = open("access_save.log", "a")

        log_data = {"status": True, "data": []}
        for line in new_logs_access:
            storage_log_access.write(line)
            log_data["data"].append(base64.b64encode(line))

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


if __name__ == '__main__':
    manager.add_command("runserver", Server(use_debugger=True, host='localhost', port=5000))
    manager.run()
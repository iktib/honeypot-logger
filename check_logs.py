import os, time, requests, re

ip_honeypot = '52.59.188.37'
host = "http://192.168.43.221"
port = "3000"
path = "/api/honeyActivity/alert"

Main_Server = host + ":" + port + path
addrs = []
size_file = 1
while True:

    if size_file == 0 or os.path.getsize("access.log") == size_file:

        time.sleep(5)
    else:
        size_file = os.path.getsize("access.log")
        file = open("access.log")
        for line in file:
            addrs.append(re.findall(r'([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', line)[0])
        unique_addr = []
        for i in addrs:
            if i not in unique_addr:
                unique_addr.append(i)
        for ip_port in unique_addr:
            requests.post(Main_Server, data={"ipHoneypot": ip_honeypot, "ipHacker": ip_port})
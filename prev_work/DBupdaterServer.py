'''
    not working 
'''
# broken pipe error, most likely didn't parse JSON properly
# Traceback (most recent call last):
#   File "DBupdaterServer.py", line 26, in <module>
#     soc.sendall(data)
# BrokenPipeError: [Errno 32] Broken pipe

import socket
import json
import time

FILE_PATH = "planeDB.json"

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

soc.bind(("127.0.0.1", 1134))
soc.listen(1)

def getData():
    with open(FILE_PATH) as json_file:
        data = json.dumps( json.load(json_file))
        data = bytes(data, 'utf-8')
        # data = json.load(json_file)
        return data
        
data = getData()
# print((data))
# print(len(data))

while True:
    clientsoc, address = soc.accept()
    # socket.send('%d\n' % len(data))
    soc.sendall(data)
    # clientsoc.send(bytes('ahh hwllo', 'utf-8'))
    time.sleep(2000)
    clientsoc.close()
    # break





# from jsonsocket import Client, Server

# host = 'localhost'
# port = 8000

# # Server code:
# server = Server(host, port)
# server.accept()
# data = server.recv()
# # data now is: {'some_list': [123, 456]}
# server.send({'data': data}).close()
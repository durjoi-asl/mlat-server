import socket
import json

FILE_PATH = "planeDB.json"

soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

soc.bind(("127.0.0.1", 1234))
soc.listen(5)

def getData():
    with open(FILE_PATH) as json_file:
        # return json.load(json_file)
        return json_file
data = getData()

while True:
    soc.send(data)
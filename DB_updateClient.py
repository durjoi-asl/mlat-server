import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 1134))

msg = s.recv(1024)
print(msg.decode("utf-8"))





# from  jsonsocket import Client

# host = 'localhost'
# port = 8000


# # Client code:
# client = Client()
# client.connect(host, port).send({'some_list': [123, 456]})
# response = client.recv()
# # response now is {'data': {'some_list': [123, 456]}}
# client.close()


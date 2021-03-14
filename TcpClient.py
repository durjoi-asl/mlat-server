import socket 
import threading 
from Decoder import Decoder

ALL_MESSAGES = []


class TcpClient():
    def __init__(self, host, port, buffersize = 4096):
        super(TcpClient, self).__init__()
        
        self.host = host
        self.port = port
        self.buffer = []
        self.socket = None
        self.buffersize = buffersize
        self.threadList = []

    def handle_connection(self, host, thread_id):
        addr = (host, self.port)
        
        self.socket.connect(addr)
        
        while True: 
            data = self.socket.recv(self.buffersize)
            print(f"[DATA PACKET] ------ {host} ----- {thread_id} \n")
            # print(format(data))
            # print("\n")
            decoder = Decoder(data)
            decoder.handle_decode()
            messages_mlat = decoder.handle_messages()
            
            for msg in messages_mlat:
                if msg[0] in ALL_MESSAGES:
                    
                    print(msg[0] + " " + ALL_MESSAGES[ALL_MESSAGES.index(msg[0])])
                else: 
                    print("Not in")
                ALL_MESSAGES.append(msg[0])
            
    def handle_thread(self):
        
        for i, host_ip in enumerate(self.host): 
            newThread = threading.Thread(target=self.handle_connection, args=(host_ip, i+1))
            
            self.threadList.append(newThread)
    
    def run(self): 
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Preparing thread
        self.handle_thread()

        # Starting all thread
        for thread in self.threadList:
            
            thread.start()

            print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")
            
client = TcpClient(["192.168.30.27", "192.168.101.3"], 10004)
client.run()
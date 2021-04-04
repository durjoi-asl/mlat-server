from http.server import HTTPServer, BaseHTTPRequestHandler
# import BaseHttp
## https doesn't work, work on that later

import json

# localhost = 127.0.0.1

FILE_PATH = "planeDB.json"

def getData():
    with open(FILE_PATH) as json_file:
        # data = json.dumps(json.load(json_file)).encode() #.encode doesn't work
        # data = '['+json.dumps(json.load(json_file))+']'
        
        data = json.dumps(json.load(json_file))
        print(type(data))
        # json.dumps(display).encode()
        
        #data = json.load(json_file)
        data = bytes(data, 'utf-8')
        # data = json.load(json_file)
        # print('data: ',data)
        print("Sending data ")
        return data

class getPlaneInfo(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(getData())
        # self.wfile.write("hello world")

def main():
    PORT = 8001
    # PORT = 3006
    server = HTTPServer(('', PORT), getPlaneInfo)
    print('Server running on port %s' %PORT)
    server.serve_forever()

if __name__ == '__main__':
    main()
    
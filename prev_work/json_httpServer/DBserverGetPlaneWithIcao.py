'''
    API end point that sends airplane information for a particular ICAO number from planeDB
'''
from http.server import HTTPServer, BaseHTTPRequestHandler
from DBmongoDB.DB_handler import mongoDBClass
from urllib.parse import urlparse
import json

hostName = "localhost"
# localhost = 127.0.0.1
mongo_obj = mongoDBClass(0,0)


        
def getDBData(msg_icao):
    '''
        connects to mongoDB, retreives plane with matching icaoNo and its relevant info
    '''
    data = mongo_obj.getPlaneByIcao(msg_icao)
    print(data)
    data = bytes(data, 'utf-8')
    print(data)
    print(type(data))
    return data

class getPlaneInfo(BaseHTTPRequestHandler):
    def do_GET(self):

        query = urlparse(self.path).query.split("=")
        # if query[0] == ''
        print(query)
        if query[0] == 'icao':
            self.send_response(200)
            self.send_header('content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            # getDBData()
            # self.wfile.write(getData())
            self.wfile.write(getDBData(query[1]))
            # self.wfile.write("hello world")
        else:
            self.send_response(200)
            self.send_header('content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(bytes("wrong parameter given", 'utf-8'))


def main():
    PORT = 8002
    # PORT = 3006
    server = HTTPServer(('', PORT), getPlaneInfo)
    print("server endpoint to get info of a particular icao assigned aircraft")
    print('Server running on port %s' %PORT)
    # server.serve_forever()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    server.server_close()
    print("Server stopped.")

if __name__ == '__main__':
    main()
    
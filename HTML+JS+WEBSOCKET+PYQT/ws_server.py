import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket
import json
import Adafruit_DHT
#import Application
#from Application import last_ten_val
import proj1 as pr


'''
This is a simple Websocket Echo server that uses the Tornado websocket handler.
Please run `pip install tornado` with python of version 2.7.9 or greater to install tornado.
This program will echo back the reverse of whatever it recieves.
Messages are output to the terminal for debuggin p                      urposes. 
''' 
DHT_SENSOR = Adafruit_DHT.DHT22 
DHT_PIN = 4
 
class WSHandler(tornado.websocket.WebSocketHandler):
   
    def open(self):
        print('new connection')
    #When message is recieved from a client call this function and connection is open 
    def on_message(self, message):
        
        if message == "Current values request from client":
            print('message received:',message)
            humidity,temperature = Adafruit_DHT.read_retry(DHT_SENSOR,DHT_PIN)
            humidity = round(humidity , 2) 
            temperature = round(temperature , 2)
            #self.write_message(str(humidity))
            dict_curr_val = {"Temperature": temperature, "Humidity": humidity}
           # send_data = json.dumps(dict_curr_val)
            self.write_message(json.dumps(dict_curr_val))
            
        elif message == "last ten values fron the python application":
            humid_ten1 = pr.last_ten_val()
            print(humid_ten1)
            self.write_message(str(humid_ten1))
            
        
            
            
            
            #self.write_message(str(temperature))
       # message = "Server:"+ message 
       # print('sending back message:',message)
        #send message from serverr to client
        #self.write_message(message)
     
        #self.write_message(str(humidity))
        #self.write_message(str(temperature))
    #When message is recieved from a client call this function and connection is close 
    def on_close(self):
        print('connection closed')
 
    def check_origin(self, origin):
        return True
 
application = tornado.web.Application([
    (r'/ws', WSHandler),
])
 
 
if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    myIP = socket.gethostbyname(socket.gethostname())
    print('*** Websocket Server Started at***',myIP)
    tornado.ioloop.IOLoop.instance().start()

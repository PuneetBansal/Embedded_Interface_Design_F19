'''
Name		:GuiPrac.py
Author		:Puneet Bansal and Amogh Shrikhande
Description	:Graphical User Interface using Qt5 and MySQL on Raspberry Pi 3 to talk to DHT22 
				Temperature and Humidity Sensor and graphical representation using matplotlib. 
References 	:
			MySQL link : https://pimylifeup.com/raspberry-pi-mysql/  
			Python MYSql link : https://www.w3schools.com/python/python_mysql_create_db.asp
			for timestamp: https://www.pythonforbeginners.com/basics/python-datetime-timedelta/
			temperature sensor: https://pimylifeup.com/raspberry-pi-humidity-sensor-dht22/
			matplotlib: https://matplotlib.org/tutorials/introductory/pyplot.html
			primary key :http://www.mysqltutorial.org/mysql-primary-key/
			Qtimer: https://doc.qt.io/qtforpython/PySide2/QtCore/QTimer.html
			python: https://www.geeksforgeeks.org/python-programming-language/

'''

# Imports for the program.
import mysql.connector 	#connector to work with sql database
import Adafruit_DHT 	#for the temp and humidity sensor
import threading 		#for timer
import datetime 		#for timestamp
from PyQt5 import QtWidgets
#from practiceDesign import Ui_MainWindow
from GuiFile import Ui_MainWindow
import sys
import matplotlib
import matplotlib.pyplot as plt
import numpy
from PyQt5.QtCore import QTimer
import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import threading
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import socket
import json
import Adafruit_DHT
import asyncio

#global variables
DHT_SENSOR = Adafruit_DHT.DHT22 
DHT_PIN = 4
last_ten_entries = [1, 2, 3, 4, 5, 6, 7, 8 ,9, 10]
i=0
j=0
k=0
l=0
timercount =0
celsius=1
#visit=1

#MySQL database credentials
mydb = mysql.connector.connect(
	host = "localhost",
	user = "ashvathama",
	passwd = "puneet28",
	database = "tempAndHumid"
)
mydb1 = mysql.connector.connect(
	host = "localhost",
	user = "ashvathama",
	passwd = "puneet28",
	database = "tempAndHumid"
	)
mycursor = mydb.cursor()
mycursor1 = mydb1.cursor()

mycursor.execute("CREATE TABLE IF NOT EXISTS tempAndHumidValues (ID INT(11) NOT NULL AUTO_INCREMENT, timestamp VARCHAR(255) NOT NULL , temp VARCHAR(255), humid VARCHAR(255), PRIMARY KEY (ID))")
sql = "INSERT INTO tempAndHumidValues (temp, humid, timestamp) VALUES (%s, %s, %s)"


def thread_function(name):
    asyncio.set_event_loop(asyncio.new_event_loop())
    http_server = tornado.httpserver.HTTPServer(app1)
    http_server.listen(8888)
    myIP = socket.gethostbyname(socket.gethostname())
    #print('*** Websocket Server Started at***',myIP)
    tornado.ioloop.IOLoop.instance().start()
 
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
            humid_ten1 = last_ten_val(mycursor1)
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
 
app1 = tornado.web.Application([
    (r'/ws', WSHandler),
])




def last_ten_val(mycursor2):
		j=0
		humid_ten = [0,0,0,0,0,0,0,0,0,0]
		mycursor2.execute("SELECT humid FROM tempAndHumidValues order by ID desc limit 10")
		view = mycursor2.fetchall()
		humid =()
		#faren = [0,0,0,0,0,0,0,0,0,0]
		for j in view:
			humid = humid +j
		npArray = np.array(humid).astype(np.float)
		for count in range(0,10):
			humid_ten[count] = npArray[count]
		
		print(humid_ten)
		'''for x in range(0,10):
			humidity,temperature = Adafruit_DHT.read_retry(DHT_SENSOR,DHT_PIN)
			humid_ten[x] = humidity
			print (str(humid_ten[x])+ "\n")'''
		return humid_ten
	
			
			
			
			

						
class mywindow(QtWidgets.QMainWindow): 
	global mycursor,temp1,humid,i,j,sql,celsius,k,l
		
#	@param	: self
#	@desc	: Function that gets called when Get Value button is pressed.Takes humidity and temperature 
#				values from the sensor and retries for 5 times if it is not able to fetch value. if the 
#					values is not NULL, then the temperature (in C or F), humidity and timestamp values are updated 
#						on the GUI

	def GetValueButtonFxn(self):
		global celsius
		print("GetValueButtonClicked")
		#self.ui.label.setText("Button Clicked")
		self.ui.plainTextEdit_2.setPlainText("Get Values button pressed")
		humidity,temperature = Adafruit_DHT.read(DHT_SENSOR,DHT_PIN)

		if humidity is None and temperature is None:
			for try_to_get_temp in range(0,5):
				humidity,temperature = Adafruit_DHT.read(DHT_SENSOR,DHT_PIN)
				if humidity is not None and temperature is not None:
					break
					
		if temperature is not None and humidity is not None:
			humidity = round(humidity , 2) 
			temperature = round(temperature , 2)
			timestamp = datetime.datetime.now()
			self.ui.labelHumidOutput.setText(str(humidity))
			self.ui.labelTimestampOut.setText(str(timestamp))
			if celsius==1:
				self.ui.labelTempOutput.setText(str(temperature))
			else:
				self.ui.labelTempOutput.setText(str((temperature*9/5) + 32))
		else:
			timestamp = datetime.datetime.now()
			self.ui.labelHumidOutput.setText("-")
			self.ui.labelTimestampOut.setText("-")
			self.ui.labelTempOutput.setText("-")



#	@param	: self
#	@desc	: Function that gets called when GetHumidityGraph button is pressed.Fetches the last 10
#				humidity values from the database and plots a graph using matplotlib. 

	
	def HumidityGraphFxn(self):
		print("HumidityGraphFunctionClicked")
		self.ui.plainTextEdit_2.setPlainText("Get Humidity Graph button pressed")
		humid = ()
		mycursor.execute("SELECT humid FROM tempAndHumidValues order by ID desc limit 10")
		view = mycursor.fetchall()
		for j in view:
			humid = humid +j
	
		plt.plot(last_ten_entries,humid)
		plt.xlabel('Last values')
		plt.ylabel('Humidity')
		plt.show()
	

# @param	: self 
# @desc		: Function that gets called when GetTemperatureGraph button is pressed.Fetches the last 10
#				temperature values from the database and plots a graph using matplotlib. 
	

	def temp_graph(self):
		self.ui.plainTextEdit_2.setPlainText("Get Temperature Graph button pressed")
		mycursor.execute("SELECT temp FROM tempAndHumidValues order by ID desc limit 10")
		view = mycursor.fetchall()
		temp1 =()
		faren = [0,0,0,0,0,0,0,0,0,0]
		for j in view:
			temp1 = temp1 +j
		print(temp1)
		npArray = np.array(temp1).astype(np.float)
		for count in range(0,9):
			faren[count] = ((float(npArray[count])*1.8) + float(32))
			
		if celsius==1:
			plt.plot(last_ten_entries,temp1)
			plt.xlabel('Last 10 values')
			plt.ylabel('Temperature(°C)')
			plt.show()
		else:
			plt.plot(last_ten_entries,faren)
			plt.xlabel('Last 10 values')
			plt.ylabel('Temperature(°F)')
			plt.show()


#	@param	: self
#	@desc	: Function that gets called when SetThreshold button is pressed.Takes user input of the temperature
#				and humidity threshold and compares it to the newly fetched temperature and humidity values. Displays
#					alarm message if the temp &/or humid values is above the threshold.
	
				
	def checkAlarm(self):
		self.ui.plainTextEdit_2.setPlainText("Set threshold button pressed")
		tempThreshold = self.ui.lineEditTempThreshold.text()
		humidThreshold = self.ui.lineEditHumidThreshold.text()
		humidity,temperature = Adafruit_DHT.read_retry(DHT_SENSOR,DHT_PIN)
		print(tempThreshold)
		print(humidThreshold)
		
		if temperature is not None and humidity is not None:
			humidity = round(humidity , 2)
			temperature = round(temperature , 2)
			print("Temp threshold is ",tempThreshold)
			print("Humid threshold is ",humidThreshold)
			print("humidity is",humidity)
			if celsius ==1:
				if((temperature > float(tempThreshold)) and (humidity > float(humidThreshold))):
					self.ui.DisplayAlarm.setText("Both Temperature and Humidity Above Threshold")
				elif(humidity > float(humidThreshold)):
					self.ui.DisplayAlarm.setText("Humidity Above Threshold")		
				elif(temperature > float(tempThreshold)):
					self.ui.DisplayAlarm.setText("Temperature Above Threshold")
				else:
					self.ui.DisplayAlarm.setText("Normal values")
			else :
				tempFar= ((temperature*9/5) + 32)
				if((tempFar > float(tempThreshold)) and (humidity > float(humidThreshold))):
					self.ui.DisplayAlarm.setText("Both Temperature and Humidity Above Threshold")
				elif(humidity > float(humidThreshold)):
					self.ui.DisplayAlarm.setText("Humidity Above Threshold")		
				elif(tempFar > float(tempThreshold)):
					self.ui.DisplayAlarm.setText("Temperature Above Threshold")
				else:
					self.ui.DisplayAlarm.setText("Normal values")
					
		else:
			self.ui.DisplayAlarm.setText("Sensor value temporarily unavailable")	
						

#	@param	: self, temperature, humidity and timestamp 
#	@desc	: This function updates the new values of threshold, timestamp, temperature and humidity on the GUI 
#			which are obtained after the 15 second timer expires.

	
	def update_readings(self,temperature,humidity,timestamp):
		print("Check")	
		global celsius	
		if temperature is not None and humidity is not None:
			tempThreshold = self.ui.lineEditTempThreshold.text()
			humidThreshold = self.ui.lineEditHumidThreshold.text()
			print(tempThreshold)
			print(humidThreshold)
			print("humidity in update reading is",humidity)
		
			self.ui.DisplayCurrentValue_Status.setText("Sensor Connected")
			
			if celsius==1:
				print("humidity in celsius in update reading is",humidity)
				self.ui.DisplayCurrentValue_Temp.setText(str(temperature))
				if ((temperature > float(tempThreshold)) and (humidity > float(humidThreshold))):
					self.ui.DisplayAlarm.setText("Both Temperature and Humidity Above Threshold")	
				elif (humidity > float(humidThreshold)):
					self.ui.DisplayAlarm.setText("Humidity Above Threshold")		
				elif (temperature > float(tempThreshold)):
					self.ui.DisplayAlarm.setText("Temperature Above Threshold")
				else:
					self.ui.DisplayAlarm.setText("Normal values")
				
			else:
				print("humidity in far in update reading is",humidity)
				self.ui.DisplayCurrentValue_Temp.setText(str((temperature*9/5) + 32))
				tempFar= ((temperature*9/5) + 32)
				if ((tempFar > float(tempThreshold)) and (humidity > float(humidThreshold))):
					self.ui.DisplayAlarm.setText("Both Temperature and Humidity Above Threshold")
				elif (humidity > float(humidThreshold)):
					self.ui.DisplayAlarm.setText("Humidity Above Threshold")		
				elif (tempFar > float(tempThreshold)):
					self.ui.DisplayAlarm.setText("Temperature Above Threshold")
				else:
					self.ui.DisplayAlarm.setText("Normal values")
			
			self.ui.DisplayCurrentValue_Humid.setText(str(humidity))
			self.ui.DisplayCurrentValue_Timestamp.setText(str(timestamp))
		else:	
			self.ui.DisplayCurrentValue_Status.setText("Sensor Disonnected")
			self.ui.DisplayCurrentValue_Temp.setText("NA")
			self.ui.DisplayCurrentValue_Humid.setText("NA")
			self.ui.DisplayCurrentValue_Timestamp.setText("NA")


#	@param	: self
#	@desc	: Function that gets called when the 15 second timer gets expired. This function takes new readings
#				of temperature and humidity and updates the values to the GUI by calling update_readings function.
		
		
	def timercheck(self):
		global timercount,my_timer

		if timercount == 30:
			print('Max count reached')
			self.timer.stop()
			sys.exit()
			
		else:		
			print("Entered timer")
			timercount += 1
			humidity,temperature = Adafruit_DHT.read(DHT_SENSOR,DHT_PIN)
			timestamp = datetime.datetime.now()
			if humidity is None and temperature is None:
				for try_to_get_temp in range(0,5):
					humidity,temperature = Adafruit_DHT.read(DHT_SENSOR,DHT_PIN)
					if humidity is not None and temperature is not None:
						break
					
			
			if temperature is not None and humidity is not None:
				humidity = round(humidity , 2)
				temperature = round(temperature , 2)			
				val = (temperature,humidity,timestamp)
				mycursor.execute(sql,val)
				mydb.commit()
				application.update_readings(temperature,humidity,timestamp)
				print(mycursor.rowcount, "record inserted.", 'temp =',temperature,"humid=",humidity)
			else:

				application.update_readings(None,None,timestamp)
				
				
	def last_ten_val(self):
		humid_ten = ()
		mycursor.execute("SELECT humid FROM tempAndHumidValues order by ID desc limit 10")
		view = mycursor.fetchall()
		for k in view:
			humid = humid +k
		timestamp_ten = ()
		mycursor.execute("SELECT timestamp FROM tempAndHumidValues order by ID desc limit 10")
		view = mycursor.fetchall()
		for l in view:
			timestamp_ten = timestamp_ten +l
	
		

#	@param	: self
#	@desc	: Function that performs the conversion from celsius and farhenheit and vice versa
			
	def celsius_farenhiet_convert(self):
		global celsius
		celsius =not celsius
		self.ui.plainTextEdit_2.setPlainText("C-F/F-C button pressed")
		humidity,temperature = Adafruit_DHT.read(DHT_SENSOR,DHT_PIN)
		if humidity is None and temperature is None:
			for try_to_get_temp in range(0,5):
				humidity,temperature = Adafruit_DHT.read(DHT_SENSOR,DHT_PIN)
				if humidity is not None and temperature is not None:
					break
		
		if celsius==0 and temperature is not None:
			self.ui.Temp_units.setText("F")
			temporary=self.ui.lineEditTempThreshold.text()
			temp1 = float(temporary)
			temporary1=((temp1*1.8) + 32.00)
			self.ui.lineEditTempThreshold.setText(str(temporary1))
			self.ui.labelTempOutput.setText(str((float(temperature)*1.8) + float(32)))
			self.ui.DisplayCurrentValue_Temp.setText(str((temperature*9/5) + 32))
			
		elif temperature is not None:
			temporary=self.ui.lineEditTempThreshold.text()
			self.ui.Temp_units.setText("C")
			temporary2= ( (0.555) * (float(temporary)-32.00))
			temporary2 = round(temporary2)
			self.ui.lineEditTempThreshold.setText(str(temporary2))			
			self.ui.labelTempOutput.setText(str(temperature))
			self.ui.DisplayCurrentValue_Temp.setText(str(temperature))
			

#	@param	: self
#	@desc	: Constructor that connects the signals from button presses to the function that needs 
#				to be called when the signal is received. Apart ffrom this the Qtimer is also initialised
#					to be called after every 15 seconds. 
	
		
	def __init__(self):	 
		super(mywindow, self).__init__()
		self.ui = Ui_MainWindow()		
		self.ui.setupUi(self)
		self.ui.GetValueButton.clicked.connect(lambda: self.GetValueButtonFxn())
		self.ui.SetThresholdButton.clicked.connect (lambda:  self.checkAlarm())
		self.ui.radioButton_Temp.pressed.connect(lambda: self.temp_graph())
		self.ui.radioButton_Humid.pressed.connect(lambda: self.HumidityGraphFxn())		
		self.ui.Celsius_farenhiet.clicked.connect(lambda: self.celsius_farenhiet_convert())
		self.timer = QTimer()
		self.timer.timeout.connect(self.timercheck)
		self.timer.start(15000)
		self.ui.Temp_units.setText("C")
		self.ui.lineEditTempThreshold.setText(str(30))
		self.ui.lineEditHumidThreshold.setText(str(55))

app = QtWidgets.QApplication([])
application = mywindow()
application.show()

x = threading.Thread(target=thread_function, args=(1,))
x.start()

sys.exit(app.exec_())
x.join()



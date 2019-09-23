import mysql.connector #connector to work with sql database
import Adafruit_DHT #for the temp and humidity sensor
import threading #for timer
import datetime #for timestamp
from PyQt5 import QtWidgets
from practiceDesign import Ui_MainWindow
import sys
import matplotlib
import matplotlib.pyplot as plt
import numpy
import multitimer
from PyQt5.QtCore import QTimer
import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
#from practiceDesign import *

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4
last_ten_entries = [1, 2, 3, 4, 5, 6, 7, 8 ,9, 10]
#temp = [23.4, 10, 22.56, 43, 13, 15, 18, 22.87, 37, 12]

mydb = mysql.connector.connect(
	host = "localhost",
	user = "ashvathama",
	passwd = "puneet28",
	database = "tempAndHumid"
)

mycursor = mydb.cursor()
sql = "INSERT INTO tempAndHumidValues (temp, humid, timestamp) VALUES (%s, %s, %s)"
i=0
j=0
timercount =0
#celsius=1
celsius=1
'''
def myTimer():
		global count,my_timer
		if count == 10:
			print('Max count reached')
			my_timer.cancel()
		else:		
			print("Entered timer")
			count += 1
			my_timer.cancel()
			my_timer = threading.Timer(2.0,myTimer)
			humidity,temperature = Adafruit_DHT.read_retry(DHT_SENSOR,DHT_PIN)
			humidity = round(humidity , 2)
			temperature = round(temperature , 2)
			timestamp = datetime.datetime.now()
			val = (temperature,humidity,timestamp)
			mycursor.execute(sql,val)
			mydb.commit()
			application.update_readings(temperature,humidity,timestamp)
			print(mycursor.rowcount, "record inserted.", 'temp =',temperature,"humid=",humidity)
			my_timer.start()


def job():
	print("Inside timer")
	global sql,mycursor
	humidity,temperature = Adafruit_DHT.read_retry(DHT_SENSOR,DHT_PIN)
	humidity = round(humidity , 2)
	temperature = round(temperature , 2)
	timestamp = datetime.datetime.now()
	val = (temperature,humidity,timestamp)
	mycursor.execute(sql,val)
	mydb.commit()
	application.update_readings(temperature,humidity,timestamp)
	print(mycursor.rowcount, "record inserted.", 'temp =',temperature,"humid=",humidity)
'''
class mywindow(QtWidgets.QMainWindow): 
	global mycursor,temp1,humid,i,j,sql,celsius
	
	
	def GetValueButtonFxn(self):
		global celsius
		print("GetValueButtonClicked")
		#self.ui.label.setText("Button Clicked")
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
			
			
	#def TemperatureGraphFxn(self):
	#	print("TemperatureGraphFunctionClicked")
		
	
	def HumidityGraphFxn(self):
		print("HumidityGraphFunctionClicked")
		self.ui.graphics_graph.clear()
		humid = ()
		mycursor.execute("SELECT humid FROM tempAndHumidValues order by ID desc limit 10")
		view = mycursor.fetchall()
		for j in view:
			humid = humid +j
		npArray = np.array(humid).astype(np.float)
		self.ui.graphics_graph.plot(npArray)
		
		
		#plt.plot(last_ten_entries,humid)
		#plt.xlabel('Last values')
		 #plt.ylabel('Humidity')
		#plt.show()
		
	def temp_graph(self):
		self.ui.graphics_graph.clear()
		mycursor.execute("SELECT temp FROM tempAndHumidValues order by ID desc limit 10")
		view = mycursor.fetchall()
		temp1 =()
		#faren=[float]*len(last_ten_entries)
		faren = [0,0,0,0,0,0,0,0,0,0]
		for j in view:
			temp1 = temp1 +j
		print(temp1)
		npArray = np.array(temp1).astype(np.float)
		
		
		for count in range(0,9):
			faren[count] = ((float(npArray[count])*1.8) + float(32))
		
		
		#L=[None]*len(last_ten_entries)
		
		
		#for count in range (0,9):
		#	L[count] = float(temp1[count])
			
		#L=[1,2,3,4,5]
		if celsius==1:
			self.ui.graphics_graph.plot(npArray)
		else:
			self.ui.graphics_graph.plot(faren)
			

		#plt.plot(last_ten_entries,temp1)
		
		#plt.ylabel('Temperature')
		#plt.show()
		
	def checkAlarm(self):
		tempThreshold = self.ui.lineEditTempThreshold.text()
		humidThreshold = self.ui.lineEditHumidThreshold.text()
		humidity,temperature = Adafruit_DHT.read_retry(DHT_SENSOR,DHT_PIN)
		
		if temperature is not None and humidity is not None:
			humidity = round(humidity , 2)
			temperature = round(temperature , 2)
			print("Temp threshold is ",tempThreshold)
			print("Humid threshold is ",humidThreshold)
			if(humidity > float(humidThreshold)):
				self.ui.DisplayAlarm.setText("Above Threshold")		
			if(temperature > float(tempThreshold)):
				self.ui.DisplayAlarm.setText("Above Threshold")
			else:
				self.ui.DisplayAlarm.setText("Normal values")
		else:
			self.ui.DisplayAlarm.setText("Sensor value temporarily unavailable")	
						
	
	def update_readings(self,temperature,humidity,timestamp):
		print("Check")	
		global celsius	
		#self.ui.plainTextEdit1.setPlainText(str(temperature))
		if temperature is not None and humidity is not None:
			'''tempThreshold = self.ui.lineEditTempThreshold.text()
			humidThreshold = self.ui.lineEditHumidThreshold.text()
			if(humidity > float(humidThreshold)):
				self.ui.DisplayAlarm.setText("Above Threshold")		
			if(temperature > float(tempThreshold)):
				self.ui.DisplayAlarm.setText("Above Threshold")
			else:
				self.ui.DisplayAlarm.setText("Normal values")'''
		
			self.ui.DisplayCurrentValue_Status.setText("Sensor Connected")
			if celsius==1:
				self.ui.DisplayCurrentValue_Temp.setText(str(temperature))
			else:
				self.ui.DisplayCurrentValue_Temp.setText(str((temperature*9/5) + 32))
			self.ui.DisplayCurrentValue_Humid.setText(str(humidity))
			self.ui.DisplayCurrentValue_Timestamp.setText(str(timestamp))
		else:	
			self.ui.DisplayCurrentValue_Status.setText("Sensor Disonnected")
			self.ui.DisplayCurrentValue_Temp.setText("NA")
			self.ui.DisplayCurrentValue_Humid.setText("NA")
			self.ui.DisplayCurrentValue_Timestamp.setText("NA")
		
		
	def timercheck(self):
		global timercount,my_timer
		#temperature = 0.00
		#humidity = 0.00
		if timercount == 10:
			print('Max count reached')
			self.timer.stop()
			sys.exit()
			
		else:		
			print("Entered timer")
			timercount += 1
			#humidity,temperature = Adafruit_DHT.read_retry(DHT_SENSOR,DHT_PIN)
			humidity,temperature = Adafruit_DHT.read(DHT_SENSOR,DHT_PIN)
			timestamp = datetime.datetime.now()
			if humidity is None and temperature is None:
				for try_to_get_temp in range(0,5):
					humidity,temperature = Adafruit_DHT.read(DHT_SENSOR,DHT_PIN)
					if humidity is not None and temperature is not None:
						break
					
			
			if temperature is not None and humidity is not None:
			#if reading is acquired do store the val and do whatever you want else 
			#read again until you get a value
				humidity = round(humidity , 2)
				temperature = round(temperature , 2)			
				val = (temperature,humidity,timestamp)
				mycursor.execute(sql,val)
				mydb.commit()
				application.update_readings(temperature,humidity,timestamp)
				print(mycursor.rowcount, "record inserted.", 'temp =',temperature,"humid=",humidity)
			else:
				application.update_readings(None,None,timestamp)
				
			
	def celsius_farenhiet_convert(self):
		global celsius
		celsius =not celsius
		humidity,temperature = Adafruit_DHT.read(DHT_SENSOR,DHT_PIN)
		if humidity is None and temperature is None:
			for try_to_get_temp in range(0,5):
				humidity,temperature = Adafruit_DHT.read(DHT_SENSOR,DHT_PIN)
				if humidity is not None and temperature is not None:
					break
					
		if celsius==0 and temperature is not None:
			self.ui.Temp_units.setText("F")
			#celsius =not celsius
			self.ui.labelTempOutput.setText(str((float(temperature)*1.8) + float(32)))
		elif temperature is not None:
			self.ui.Temp_units.setText("C")
			#celsius =not celsius
			self.ui.labelTempOutput.setText(str(temperature))
		
#		if celsius==1:
#			self.ui.labelTempOutput.setText(str(temperature))
#			celsius=0
#		elif celsius==0:
#			self.ui.labelTempOutput.setText(str((temperature*1.8) + 32))
#			celsius=1
		
	def __init__(self):	 
		super(mywindow, self).__init__()
		self.ui = Ui_MainWindow()		
		self.ui.setupUi(self)
		self.ui.GetValueButton.clicked.connect(lambda: self.GetValueButtonFxn())
		#self.ui.TemperatureGraph.clicked.connect(lambda: self.TemperatureGraphFxn())
		#self.ui.HumidityGraph.clicked.connect(lambda: self.HumidityGraphFxn())
		#self.ui.GetTemperatureGraphButton.clicked.connect (lambda:  self.temp_graph())
		self.ui.SetThresholdButton.clicked.connect (lambda:  self.checkAlarm())
		self.ui.radioButton_Temp.pressed.connect(lambda: self.temp_graph())
		self.ui.radioButton_Humid.pressed.connect(lambda: self.HumidityGraphFxn())		
		self.ui.Celsius_farenhiet.clicked.connect(lambda: self.celsius_farenhiet_convert())
		#self.ui.graphics_graph.clicked.connect(lambda: self.celsius_farenhiet_convert())
		self.timer = QTimer()
		self.timer.timeout.connect(self.timercheck)
		self.timer.start(15000)
		self.ui.Temp_units.setText("C")



app = QtWidgets.QApplication([])
application = mywindow()
application.show()
#timer = multitimer.MultiTimer(interval=3, function=job, count=10,runonstart=True)
#timer.start()

#my_timer = threading.Timer(2.0,myTimer)
#my_timer.start()

#timer.stop()
sys.exit(app.exec_())


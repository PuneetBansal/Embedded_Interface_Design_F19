'''
Name		:Application_final_proj.py
Author		:Puneet Bansal and Amogh Shrikhande

References 	:
			MySQL link : https://pimylifeup.com/raspberry-pi-mysql/  
			Python MYSql link : https://www.w3schools.com/python/python_mysql_create_db.asp
			primary key :http://www.mysqltutorial.org/mysql-primary-key/
			python: https://www.geeksforgeeks.org/python-programming-language/
'''

# Imports for the program
from PyQt5 import QtWidgets
from final_proj_test_image_new import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from mysqlLibrary import *
import mysql.connector 	#connector to work with sql database
from s3 import *


class mywindow(QtWidgets.QMainWindow):

#	@param	: self
#	@desc	: Function that is invoked when Last Image Taken button is pressed.Displays the Image downloaded from 
#                              AWS on the GUI
#							
	def show_image(self):
		downloadImage();
		self.ui.photo.setPixmap(QtGui.QPixmap("/home/pi/EID/project5/downloadedImage.jpg"))

		
#	@param	: self
#	@desc	: Function that is invoked when Fetch Image Data button is pressed. This function will calculate number of times correcto 
#			  is said 
	def image_data(self):
		correct_count = search_occurance_in_responseTable("correcto")
		total_response_count = search_all_occurance_in_responseTable()
		correct_image_percent = round(((correct_count/total_response_count)*100),2)
		wrong_image_percent = round((100 - correct_image_percent),2)
		print("Count : ")
		print(correct_image_percent)
		self.ui.correct_image_op.setText(str(correct_image_percent))
		self.ui.wrong_image_op.setText(str(wrong_image_percent))
		
#	@param	: self
#	@desc	: Function that is invoked when Fetch voice command Data button is pressed. This function will calculate number of times correcto 
#			  wrongo and identify is said by the user
		
	def voice_command_data(self):
		correct_count = search_occurance_in_responseTable("correcto")
		wrongo_count = search_occurance_in_responseTable("wrongo")
		identify_count = search_occurance_in_commandTable("identify")
		total_response_count = search_all_occurance_in_responseTable()
		total_command_count = search_all_occurance_in_commandTable()
		# Formula to count the correct voice percentage
		correct_voice_percent = round((((correct_count + wrongo_count + identify_count)/(total_command_count + total_response_count))*100),2)
		wrong_voice_percent = round((100 - correct_voice_percent),2)
		
		self.ui.correct_voice_op.setText(str(correct_voice_percent))
		self.ui.wrong_voice_op.setText(str(wrong_voice_percent))
		
#	@param	: self
#	@desc	: Function that is invoked when Get Latest Label button is pressed. This function will fetch the most 
#           recent label from the My SQL database	
	
	def get_latest_values(self):
		latest_label_name = get_latest_label()
		self.ui.lineEdit.setText(str(latest_label_name))
		
	
	
	def __init__(self):	
		super(mywindow, self).__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.ui.last_image_taken.clicked.connect(lambda: self.show_image())
		self.ui.fetch_imag_data.clicked.connect(lambda: self.image_data())
		self.ui.fetch_voice_command_data.clicked.connect(lambda: self.voice_command_data())
		self.ui.get_latest_label.clicked.connect(lambda: self.get_latest_values())


app = QtWidgets.QApplication([])
application = mywindow()
application.show()
sys.exit(app.exec_())


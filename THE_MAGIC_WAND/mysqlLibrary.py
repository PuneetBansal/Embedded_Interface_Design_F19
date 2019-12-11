# Imports for the program.
import mysql.connector 	#connector to work with sql database

#MySQL database credentials
mydb = mysql.connector.connect(
	host = "localhost",
	user = "ashvathama",
	passwd = "puneet28",
	database = "eidSuperProject")


mycursor = mydb.cursor()	

#	@param	: self
#	@desc	: Function that enables the user to create 3 tables in the same database with 1 column each
def create_tables():
	mycursor.execute("CREATE TABLE IF NOT EXISTS labelTable (ID INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, label VARCHAR(255))")
	mycursor.execute("CREATE TABLE IF NOT EXISTS commandTable (ID INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, command VARCHAR(255))")
	mycursor.execute("CREATE TABLE IF NOT EXISTS responseTable (ID INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, response VARCHAR(255))")

##	@param	: self
#	@desc	: Function that enables the user to display data 
def display_labelTable_contents():
	mycursor.execute("SELECT * FROM labelTable")
	myresult = mycursor.fetchall()
	for x in myresult:
		print(x)

#	@param	: self
#	@desc	: Function that enables the user to display data 		
def display_commandTable_contents():
	mycursor.execute("SELECT * FROM commandTable")
	myresult = mycursor.fetchall()
	for x in myresult:
		print(x)

#	@param	: self
#	@desc	: Function that enables the user to display data 
def display_responseTable_contents():
	mycursor.execute("SELECT * FROM responseTable")
	myresult = mycursor.fetchall()
	for x in myresult:
		print(x)

#	@param	: self
#	@desc	: Function that enables the user to input data in a table
def insert_into_labelTable(dataToEnter):	
	sql1 = "INSERT INTO labelTable (label) VALUES (%s)"
	dataToInsert = (dataToEnter,)
	mycursor.execute(sql1,dataToInsert)
	mydb.commit()

#	@param	: self
#	@desc	: Function that enables the user to input data in a table
def insert_into_responseTable(dataToEnter):	
	sql1 = "INSERT INTO responseTable (response) VALUES (%s)"
	dataToInsert = (dataToEnter,)
	mycursor.execute(sql1,dataToInsert)
	mydb.commit()

#	@param	: self
#	@desc	: Function that enables the user to input data in a table
def insert_into_commandTable(dataToEnter):	
	sql1 = "INSERT INTO commandTable (command) VALUES (%s)"
	dataToInsert = (dataToEnter,)
	mycursor.execute(sql1,dataToInsert)
	mydb.commit()

#	@param	: self
#	@desc	: Function that enables the user to find certain data in the label Table
def search_occurance_in_labelTable(dataToFind):
	mycursor.execute("SELECT label from labelTable")
	myresult = mycursor.fetchall()
	count =0
	for x in myresult:
		if x[0] == dataToFind:
			count = count+1
	return count

#	@param	: self
#	@desc	: Function that enables the user to get a count of all the messages in label table
def search_all_occurance_in_labelTable():
	mycursor.execute("SELECT label from labelTable")
	myresult = mycursor.fetchall()
	count =0
	for x in myresult:
		count = count+1
	return count
	
	
#	@param	: self
#	@desc	: Function that enables the user to find certain data in the command Table
def search_occurance_in_commandTable(dataToFind):
	mycursor.execute("SELECT command from commandTable")
	myresult = mycursor.fetchall()
	count =0
	for x in myresult:
		if x[0] == dataToFind:
			count = count+1
	return count
	
#	@param	: self
#	@desc	: Function that enables the user to get a count of all the messages in command table
def search_all_occurance_in_commandTable():
	mycursor.execute("SELECT command from commandTable")
	myresult = mycursor.fetchall()
	count =0
	for x in myresult:
		count = count+1
	return count

#	@param	: self
#	@desc	: Function that enables the user to find certain data in the responseTable
def search_occurance_in_responseTable(dataToFind):
	mycursor.execute("SELECT response from responseTable")
	myresult = mycursor.fetchall()
	count =0
	for x in myresult:
		if x[0] == dataToFind:
			count = count+1
	return count

#	@param	: self
#	@desc	: Function that enables the user to get a count of all the messages in response table	
def search_all_occurance_in_responseTable():
	mycursor.execute("SELECT response from responseTable")
	myresult = mycursor.fetchall()
	count =0
	for x in myresult:
		count = count+1
	return count

#	@param	: self
#	@desc	: Function that enables the user to get the latest value from the labelTable 
def get_latest_label():
	mycursor.execute("SELECT label FROM labelTable ORDER BY ID DESC LIMIT 1")
	myresult = mycursor.fetchall()
	return myresult[0][0]


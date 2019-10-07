# EID PROJECT 2
                                           Contributor : Puneet Bansal , Amogh Shrikhande
                                           Professor   : Bruce Montgomery

Python based Graphical User Interface (GUI) using QT and MySQL on Raspberry Pi 3 to talk to a DHT22 Temperature and Humidity Sensor and graphical representation using matplotlib.

## FEATURES
#### QT5 GUI
* Polls the sensor every 15 seconds to get temperature and humidity readings and stores it along with the timestamp in a MySQL database. 
* Graphical Representation of the last 10 Temperature/Humidity entries present in the database. 
* Ability to set thresholds and displays an alarm message if the temperature/humidity values are above the set threshold.
* Button Press to switch between celsius and fahrenheit. 
* Status Message displaying whether the sensor is connected or not.

#### HTML GUI
* Requests the nodeJs server and the tornado server for the latest values of temperature and humidity who in turn fetch these values from and display these values on the html page on a single button click
* Requests the nodeJs server and the tornado server for the last ten values of humidity who in turn fetch these values from MySQL database; and display these values on the html page in tabular form on a single button click
* Button press to display a graph of the last 10 humidity values fetched from the MySQL database
* Status message to report the time in ms required to fetch the last 10  humidity readings following the path: HTML->Websockets->Tornado->PythonApp->MySQL as opposed to the path: HTML->Websockets->Node.Js->MySQL

## INSTALLATION INSTRUCTIONS

#### Setting up the Pi
On a raspbian loaded pi perform these operations: 
* Connect the pi to internet using wifi or ethernet.
* Then perform these commands to update the pi with latest packages. 
  * *sudo apt-get update*
  * *sudo-apt-get-upgrade* 

#### Setting up the DHT22 sensor
* Connect a 10k ohm resistor between the VCC(Pin1 ) and Data pin(Pin2 ) of the DHT22 sensor
* Connect the VCC(3.3V) and GND pins of the sensor to the respective VCC and GND pins of the pi
* Connect the Data Pin (Pin2) of the DHT sensor with physical pin 7 (GPIO4) of the pi
* Install python3 and pip using this command 
  * *sudo apt-get install python3-dev python3-pip*
* Upgrade setuptools wheels using 
  * *sudo python3 -m pip install --upgrade pip setuptools wheel*
* Install the Adafruit DHT library:  sudo pip3 install Adafruit_DHT

#### Setting up MySQL on Raspberry Pi 
* Install MySQL server on pi using:
  * *sudo apt install mariadb-server*
* Perform MySQL securing using :
  * *sudo mysql_secure_installation*

#### Creating Database and User in MySQL
* Log into MySQL command line:
  * *sudo mysql -u root -p*
* Create Database :
  * *CREATE DATABASE tempAndHumid;*
* Create User using :
  * *CREATE USER 'ashvathama'@'localhost' IDENTIFIED BY 'puneet28';*
* Now, grant privileges to the user using :
  * *GRANT ALL PRIVILEGES ON tempAndHumid.* TO 'puneet28'@'localhost';*
* *Flush the previous privileges:*
  * *FLUSH PRIVILEGES;*

#### Using MySQL via PHP 
* *sudo apt install php-mysql*

#### Installing MatplotLib for graphs and charts
* *pip install matplotlib*

#### Installing pyqt5
* *sudo apt-get install qt5-default pyqt5-dev pyqt5-dev-tools*
* *sudo apt-get install qttools5-dev-tools*

#### Install NVM Node and NPM
* *curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.34.0/install.sh | bash*
* *nvm install 10.16.3*

#### Setting up Tornado Server
* pip *install tornado*

## HOW TO RUN THE CODE
* Clone the repository. 
* Run the bash script to set up Node js server, tornado server and the python gui:
  * *./script.sh*
* Now, run the client by clicking on Application.html

## PROJECT WORK
* Puneet
  * MySQL database setup and updating sensor data in table.
  * Integrating GUI with functions
  * Timer setup.
  * Communication between nodeJs and html client
  * Integrating HTML code for node.Js server and tornado server 
  * Embedding the graph for last ten humidity values with the HTML page
  * Multithreading in python to run QT GUI and tornado server
  * Bash script to run the QT GUI, tornado server and node.js server

* Amogh
  * Temp sensor interface
  * Graph generation using matplotlib
  * GUI installation and development 
  * Setting up tornado server 
  * Communication between tornado server and html client
  * Development of html script for html client 

## ADDITIONAL FEATURES
* Single button press to change the entire GUI from displaying any temeprature data in degree C to F and back again. 

## REFERENCES: 
* MySQL link : https://pimylifeup.com/raspberry-pi-mysql/  
* Python MYSql link : https://www.w3schools.com/python/python_mysql_create_db.asp
* For timestamp: https://www.pythonforbeginners.com/basics/python-datetime-timedelta/
* Temperature Sensor: https://pimylifeup.com/raspberry-pi-humidity-sensor-dht22/
* Matplotlib: https://matplotlib.org/tutorials/introductory/pyplot.html
* Primary Key :http://www.mysqltutorial.org/mysql-primary-key/
* Qtimer: https://doc.qt.io/qtforpython/PySide2/QtCore/QTimer.html
* Python: https://www.geeksforgeeks.org/python-programming-language/
* For communication between html client and tornado server: https://os.mbed.com/cookbook/Websockets-Server
* Tornado basic setup: http://www.tornadoweb.org/en/stable/
* Creating table on html page: https://www.youtube.com/watch?v=40qreu8Al7o 
* Converting string to javascript dictionary: https://stackoverflow.com/questions/31892971/converting-string-to-javascript-dictionary
* Shell scripting: https://stackoverflow.com/questions/28549641/run-multiple-python-scripts-concurrently
* Html graph: https://canvasjs.com/html5-javascript-line-chart/
* NodeJs talking to mysql: https://www.w3schools.com/nodejs/nodejs_mysql.asp
* NodeJs Webserver : https://www.pubnub.com/blog/nodejs-websocket-programming-examples/


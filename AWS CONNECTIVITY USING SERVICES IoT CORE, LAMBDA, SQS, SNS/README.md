# EID PROJECT 3
                                           Contributor : Puneet Bansal , Amogh Shrikhande
                                           Professor   : Bruce Montgomery

Python based Graphical User Interface (GUI) using QT and MySQL on Raspberry Pi 3 to talk to a DHT22 Temperature and Humidity Sensor and graphical representation using matplotlib.
#### ADDITION :
Client sending two types of messages from DHT22 sensor to the AWS IoT core using MQTT. First type is the data message which contains the id, the timestamp, the temperature and the humidity values collected from the DHT22 sensor and the second type is the alert message which consists of id, temperature trigger value, temperature alert value, humidity trigger value and humidity alert value. 
Lambda service of the AWS used to write a serverless process to segregate the messages from the DHT22 sensor to data messages and alert messages. The data messages are stored using the SQS queue service of AWS and the alert messages are used to trigger an alert Email. 
Client requesting temperature and humidity values from the server, which fetches these values from DHT22 sensor and displays the values in the form of tables on html page. The project is run on Rpi3 running Raspbian


## FEATURES
#### QT5 GUI
* Polls the sensor every 15 seconds to get temperature and humidity readings and stores it along with the timestamp in a MySQL database. 
* Graphical Representation of the last 10 Temperature/Humidity entries present in the database. 
* Ability to set thresholds and displays an alarm message if the temperature/humidity values are above the set threshold.
* Button Press to switch between celsius and fahrenheit. 
* Status Message displaying whether the sensor is connected or not.

#### HTML GUI
* Requests the AWS server(SQS Queue) for the latest values of timestamp, temperature and humidity who in turn fetch these values from the DHT22 temperature sensor  and display these values on the html page on a single button click
* Requests the AWS server for the latest twenty values of humidity and temperature who in turn fetch these values from DHT22 and display these values on the html page in tabular form on a single button click
* The message follows the path:
  DHT22>Python GUI>AWS IoT Core>Lambda serverless process> SQS/SNS SNS > email/message
  SQS > HTML client
  
#### AWS SERVER
* Hosts SQS, SNS and lambda services
* Recieves the data and alert messages from DHT22 using MQTT. 
* Lambda service separates the data and alert messages and sends it to SQS and SNS respectively


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

#### AWS SDK setup
pip3 install AWSIoTPythonSDK

## HOW TO RUN THE CODE
* Go to the repository where all the files have been downloaded
* run the command pthon3 Application.py
* run the client by clicking on the file Application.html

## PROJECT WORK
* Puneet
  *  MySQL database setup and updating sensor data in table.
  *  Integrating GUI with functions 
  *  Timer setup.
  *  AWS SQS and AWS SNS setup. 
  *  HTML integration with AWS SQS using AWS SDK
  *  Embedding the graph for last ten humidity values with the HTML page
  *  Multithreading in python to run QT GUI and tornado server
  *  Bash script to run the QT GUI, tornado server and node.js server

* Amogh
  * Temp sensor interface
  *  Graph generation using matplotlib and html 
  *  GUI installation and development
  *  AWS account setup
  *  AWS IoT Core (MQTT Client) setup
  *  Interface GUI (Python Application) 
  *  Html client integration with SQS using GET POST
  *  Development of html script for html client


## ADDITIONAL FEATURES
  *  Single button press to change the entire table in the GUI from displaying any temeprature data in degree C to F and back again. 
  *  Single button press to check the current message count in the queue.
  *  Single button press to change the table on the html client side from celsius to farenhiet and back again.

## ISSUES FACED
  *  Faced issues while adding the device as IoT thing on AWS, documentation did not mention to “add thing”.
  *  Less resources and documentation available for JSON 
  *  Issues faced to construct the dynamic url using the receipt handle for the queue to delete messages in the queue and hence we have used AWS API’s for the same. 
  *  Disconnected sensor outputs NULL and sends it to the queue. JSON parse unable to parse this NULL.


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
* AWS cost estimator: https://calculator.aws/#/createCalculator
* Google cost estimator: https://cloud.google.com/products/calculator/#id=f5f2327d-df63-41ac-8615-1c70d2b02d49
* SNS: https://docs.aws.amazon.com/iot/latest/developerguide/config-and-test-rules.html
* SQS AWS: https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/AWS/SQS.html#receiveMessage-property
* SQS attributes: https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-general-identifiers.html
* Actions SQS: https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_Operations.html
* Html Table: https://www.w3schools.com/tags/tag_tr.asp
* JSON documentation: https://api.jquery.com/jQuery.getJSON/
* AWS login: https://aws.amazon.com/education/awseducate/ 
* Management Console: https://console.aws.amazon.com/sqs/home?region=us-east-1



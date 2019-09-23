# GUI FOR TEMPERATURE AND HUMIDITY CONTROL USING DHT22 SENSOR
                                              Contributor : Puneet Bansal , Amogh Shrikhande
                                              Professor   : Bruce Montgomery

Python based Graphical User Interface (GUI) using QT and MySQL on Raspberry Pi 3 to talk to a DHT22 Temperature and Humidity Sensor and graphical representation using matplotlib.

## FEATURES: 
* Polls the sensor every 15 seconds to get temperature and humidity readings and stores it along with the timestamp in a MySQL database. 
* Graphical Representation of the last 10 Temperature/Humidity entries present in the database. 
* Ability to set thresholds and displays an alarm message if the temperature/humidity values are above the set threshold.
* Button Press to switch between celsius and fahrenheit. 
* Status Message displaying whether the sensor is connected or not.


## INSTALLATION INSTRUCTIONS: 

#### Setting up the Pi:
On a raspbian loaded pi perform these operations: 
* Connect the pi to internet using wifi or ethernet.
* Then perform these commands to update the pi with latest packages. 
  * *sudo apt-get update*
  * *sudo-apt-get-upgrade* 

#### Setting up the DHT22 sensor
* Connect a 10k ohm resistor between the VCC(Pin1 ) and Data pin(Pin2 ) of the DHT22 sensor
* Connect the VCC(3.3V) and GND pins of the sensor to the respective VCC and GND pins of the pi
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

#### Creating Database and User in MySQL:
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

#### Installing MatplotLib for graphs and charts:
* *pip install matplotlib*

## HOW TO RUN THE CODE :
* Clone the repository. 
* Run the file GuiPrac.py by using:
  * *python3 GuiPrac.py*
  
## PROJECT WORK:
* Puneet
  * MySQL database setup and updating sensor data in table.
  * Integrating GUI with functions
  * Timer setup.
* Amogh
  * Temp sensor interface
  * Graph generation using matplotlib
  * GUI installation and development 
  
 ## ADDITIONAL FEATURES:
 * Single button press to change the entire GUI from displaying any temeprature data in degree C to F and back again. 




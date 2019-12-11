# THE MAGIC WAND
                                           Contributor : Puneet Bansal , Amogh Shrikhande
                                           Professor   : Bruce Montgomery

A magic wand that identifies object kept infront of it and speaks out the name of identified object. Amazon lex is used for speech to text conversion, Amazon
Polly for text to speech and AWS image recognition services to detect the image. AWS SQS has been utilised to store the data in a queue.

## INSTALLATION INSTRUCTIONS

#### Setting up the Pi
On a raspbian loaded pi perform these operations: 
* Connect the pi to internet using wifi or ethernet.
* Then perform these commands to update the pi with latest packages. 
  * *sudo apt-get update*
  * *sudo-apt-get-upgrade* 

#### Setting up MySQL on Raspberry Pi 
* Install MySQL server on pi using:
  * *sudo apt install mariadb-server*
* Perform MySQL securing using :
  * *sudo mysql_secure_installation*

#### Creating Database and User in MySQL
* Log into MySQL command line:
  * *sudo mysql -u root -p*
* Create Database :
  * *CREATE DATABASE eidSuperProject;*
* Create User using :
  * *CREATE USER 'ashvathama'@'localhost' IDENTIFIED BY 'puneet28';*
* Now, grant privileges to the user using :
  * *GRANT ALL PRIVILEGES ON eidSuperProject.* TO 'puneet28'@'localhost';*
* *Flush the previous privileges:*
  * *FLUSH PRIVILEGES;*

#### Using MySQL via PHP 
* *sudo apt install php-mysql*

#### Installing pyqt5
* *sudo apt-get install qt5-default pyqt5-dev pyqt5-dev-tools*
* *sudo apt-get install qttools5-dev-tools*

#### Install NVM Node and NPM
* *curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.34.0/install.sh | bash*
* *nvm install 10.16.3*

#### AWS SDK setup
pip3 install AWSIoTPythonSDK

## HOW TO RUN THE CODE

### CLIENT SIDE
* Run *Application_client* to run the client side python script.

### SERVER SIDE
* Run *node nodeJsCode.js* to fetch the data from sqs and store it inside the mysql database.
* Run *Application_server* that starts the GUI and integrates mysql database with python.
* THe GUI has buttons to display "% correct images", "% correct voice command" and to fetch latest image and the image label recognized.

## PROJECT WORK
* Puneet
  * AWS SQS, Image Recognition, Voice Recognition Integration and Development
  * Integrating sensors and ensuring server side code integration.
  * Node JS script to fetch the data from sqs.

* Amogh
  * Create GUI (Python Application)
  * Server side code integration
  * Enable storing the data to local db via mysql and fetching data from local-db using python.

## REFERENCES: 
* MySQL link : https://pimylifeup.com/raspberry-pi-mysql/  
* Python MYSql link : https://www.w3schools.com/python/python_mysql_create_db.asp
* Python: https://www.geeksforgeeks.org/python-programming-language/
* NodeJs talking to mysql: https://www.w3schools.com/nodejs/nodejs_mysql.asp
* SQS AWS: https://docs.aws.amazon.com/AWSJavaScriptSDK/latest/AWS/SQS.html#receiveMessage-property
* AWS login: https://aws.amazon.com/education/awseducate/ 




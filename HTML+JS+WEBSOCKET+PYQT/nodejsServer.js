/*
 * Name		      : nodejsServer.js
   Author	      : Puneet Bansal and Amogh Shrikhande
   Description	: NodeJs Server that connects to HTML client. Queries the mySQL database and sends the JSON string to client.   
*/

//MySql Connection
var mysql = require('mysql');
var con = mysql.createConnection({
  host: "localhost",
  user: "ashvathama",
  password: "puneet28",
  database : "tempAndHumid"
});

//Function that gets called on getting a connection
con.connect(function(err) {
  if (err) throw err;
  console.log("Connected!");
  connected = 1;
});

const http = require('http');
const WebSocketServer = require('websocket').server;
const server = http.createServer();
server.listen(9898);
const wsServer = new WebSocketServer({
    httpServer: server
});

//Function that gets called when a message is received from the client. The message received is checked, whether the client is seeking one value or 10 values and the
//corresponsing values are sent. 

wsServer.on('request', function(request) {
    const connection = request.accept(null, request.origin);
    connection.on('message', function(message) {
      console.log('Received Message:', message.utf8Data);
      if(message.utf8Data == "last ten values fron the nodejs application")
      {
        if(connected == 1)
        {
          con.query("SELECT * FROM tempAndHumidValues order by ID desc limit 10",function(err,result,fields){
          if(err) throw err;
          console.log(result);
          JSONstring = JSON.stringify(result); 
          console.log("inside if loop");
          //connection.send("1");
          connection.send(JSONstring);
          });
        }
      }
      if(message.utf8Data == "latest values fron the nodejs application")
      {
        con.query("SELECT * FROM tempAndHumidValues order by ID desc limit 1",function(err,result,fields){
        if(err) throw err;
        console.log(result);
        JSONstring1 = JSON.stringify(result); 
        console.log(JSONstring1);
        connection.send(JSONstring1);
        });
      }
      
    });
    connection.on('close', function(reasonCode, description) {
        console.log('Client has disconnected.');
    });
});


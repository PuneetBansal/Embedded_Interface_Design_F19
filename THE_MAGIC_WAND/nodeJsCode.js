/*
Name		: nodeJsCode.js
Author		: Puneet Bansal and Amogh Shrikhande
Description	: Node Js file that fetches data from Queues in AWS and stores it in MySQL database. 
References 	: MySQL link : https://pimylifeup.com/raspberry-pi-mysql/  
		  Python MYSql link : https://www.w3schools.com/python/python_mysql_create_db.asp
		  AWS Node JS SDK : https://aws.amazon.com/sdk-for-node-js/

*/

var AWS = require("aws-sdk");
var mysql = require('mysql');
var  util = require('util');

/*AWS Queue URL's */
var IMAGE_QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/998008274670/ImageLabeQueue' ;
var VOICE_QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/998008274670/voiceInputQueue';
var VOICE_RESPONSE_URL = 'https://sqs.us-east-1.amazonaws.com/998008274670/voiceResponseQueue';

/*Configure AWS region and create an SQS service object */
AWS.config.update({region: 'REGION'});
var sqs = new AWS.SQS({apiVersion: '2012-11-05'});

/*Enabling connection to mysql*/
var con = mysql.createConnection({
	host : "localhost",
	user : "ashvathama",
	password : "puneet28",
	database : "eidSuperProject"
});
con.connect(function(err) {
  if (err) throw err;
  console.log("Connected!");
});

var loop2=0;
setInterval(getValueAndInsertIntoCommandTable,4000)


function getValueAndInsertIntoCommandTable()
{
var params = {
AttributeNames: [
    "ApproximateNumberOfMessages"
],
QueueUrl: VOICE_QUEUE_URL,
};

total_message_count=0;
sqs.getQueueAttributes(params, function(err, data) {
		  if (err) 
		  {
			console.log(err, err.stack); // an error occurred
		  }
		  else
		  {
			  console.log(data);           // successful response
			  total_message_count = data.Attributes.ApproximateNumberOfMessages;  
			  console.log("Total message count :" ,total_message_count) 
			  /******************************************************/
			  
		var loop =0;
		 while (loop < total_message_count)
		 {
			 sqs.receiveMessage(params, function(err, data) {
				if (err) 
				{
					console.log("Receive Error", err);
				} 
				else if (data.Messages) 
				{
					if(data.Messages.length !=0)
					{
					  console.log("Data Received is", (data.Messages[0].Body));
					  var data1 = data.Messages[0].Body
					  var sql = "INSERT INTO commandTable (command) VALUES ('%s')";
					  var result = util.format(sql,data1)
					  console.log(result);

					   con.query(result, function (err,result) {
						  if (err) throw err;
						  console.log("1 record inserted");     
		      
						  
					    });
					  
					  //console.log(data.Messages)
					  var deleteParams = {
					  QueueUrl: VOICE_QUEUE_URL,
					  ReceiptHandle: data.Messages[0].ReceiptHandle
					      };
					    
					    sqs.deleteMessage(deleteParams, function(err, data) {
					      if (err) 
					      {
						    console.log("Delete Error", err);
					      } 
					      else 
					      {
						    console.log("Message Deleted", data);
					      }
					    });
					  }
					  else
					  {
					  console.log("queue empty")
					  }
							
				}
					
				
				
			});
		loop = loop+1;
		}
			  
			  
			  /********************************************************/
		  
		  
		  
		  }
		 
		 /*var loop =0;
		 while (loop < total_message_count)
		 {
			 sqs.receiveMessage(params, function(err, data) {
				if (err) 
				{
					console.log("Receive Error", err);
				} 
				else if (data.Messages) 
				{
					if(data.Messages.length !=0)
					{
					  console.log("Data Received is", (data.Messages[0].Body));
					  var data = data.Messages[0].Body
					  var sql = "INSERT INTO commandTable (command) VALUES ('%s')";
					  var result = util.format(sql,data)
					  console.log(result);

					   con.query(result, function (err,result) {
						  if (err) throw err;
						  console.log("1 record inserted");
						  
					    });
					  
					  console.log("before delete param" + data.Messages[0])
					  var deleteParams = {
					  QueueUrl: VOICE_QUEUE_URL,
					  ReceiptHandle: data.Messages[0].ReceiptHandle
					      };
					    
					    sqs.deleteMessage(deleteParams, function(err, data) {
					      if (err) 
					      {
						    console.log("Delete Error", err);
					      } 
					      else 
					      {
						    console.log("Message Deleted", data);
					      }
					    });
					  }
					  else
					  {
					  console.log("queue empty")
					  }
							
				}
			/*
			var deleteParams = {
              QueueUrl: VOICE_QUEUE_URL,
              ReceiptHandle: data.Messages[0].ReceiptHandle
            };
            	
			sqs.deleteMessage(deleteParams, function(err, data) {
			  if (err) 
			  {
				console.log("Delete Error", err);
			  } 
			  else 
			  {
				console.log("Message Deleted", data);
			  }
			});
				
				
				
			});
		loop = loop+1;
		}*/
	//con.end();
});
//con.end();
getValueAndInsertIntoResponseTable();
getValueAndInsertIntoLabelTable();
}

function getValueAndInsertIntoResponseTable()
{
var params = {
AttributeNames: [
    "ApproximateNumberOfMessages"
],
QueueUrl: VOICE_RESPONSE_URL,
};

total_message_count=0;
sqs.getQueueAttributes(params, function(err, data) {
		  if (err) 
		  {
			console.log(err, err.stack); // an error occurred
		  }
		  else
		  {
			  console.log(data);           // successful response
			  total_message_count = data.Attributes.ApproximateNumberOfMessages;  
			  console.log("Total message count :" ,total_message_count) 
		  }
		 var loop =0;
		 while (loop < total_message_count)
		 {
			 sqs.receiveMessage(params, function(err, data) {
				if (err) 
				{
					console.log("Receive Error", err);
				} 
				else if (data.Messages) 
				{
					console.log("Data Received is", (data.Messages[0].Body));
					var data1 = data.Messages[0].Body
					var sql = "INSERT INTO responseTable (response) VALUES ('%s')";
					var result = util.format(sql,data1)
					console.log(result);

					  con.query(result, function (err,result) {
						if (err) throw err;
						console.log("1 record inserted");
					  });
				
					var deleteParams = {
					  QueueUrl: VOICE_RESPONSE_URL,
					  ReceiptHandle: data.Messages[0].ReceiptHandle
					};
					    
						    sqs.deleteMessage(deleteParams, function(err, data) {
						      if (err) 
						      {
							    console.log("Delete Error", err);
						      } 
						      else 
						      {
							    console.log("Message Deleted", data);
						      }
						    });
				
				}
			/*
			var deleteParams = {
              QueueUrl: VOICE_RESPONSE_URL,
              ReceiptHandle: data.Messages[0].ReceiptHandle
            };
            	
			sqs.deleteMessage(deleteParams, function(err, data) {
			  if (err) 
			  {
				console.log("Delete Error", err);
			  } 
			  else 
			  {
				console.log("Message Deleted", data);
			  }
			});*/
				
				
				
			});
		loop = loop+1;
		}
});
}


function getValueAndInsertIntoLabelTable()
{
var params = {
AttributeNames: [
    "ApproximateNumberOfMessages"
],
QueueUrl: IMAGE_QUEUE_URL,
};

total_message_count=0;
sqs.getQueueAttributes(params, function(err, data) {
		  if (err) 
		  {
			console.log(err, err.stack); // an error occurred
		  }
		  else
		  {
			  console.log(data);           // successful response
			  total_message_count = data.Attributes.ApproximateNumberOfMessages;  
			  console.log("Total message count :" ,total_message_count) 
		  }
		 var loop =0;
		 while (loop < total_message_count)
		 {
			 sqs.receiveMessage(params, function(err, data) {
				if (err) 
				{
					console.log("Receive Error", err);
				} 
				else if (data.Messages) 
				{
					console.log("Data Received is", (data.Messages[0].Body));
					var data1 = data.Messages[0].Body
					var sql = "INSERT INTO labelTable (label) VALUES ('%s')";
					var result = util.format(sql,data1)
					console.log(result);

					  con.query(result, function (err,result) {
						if (err) throw err;
						console.log("1 record inserted");
					  });
					
					  var deleteParams = {
					    QueueUrl: IMAGE_QUEUE_URL,
					    ReceiptHandle: data.Messages[0].ReceiptHandle
					  };
					      
						      sqs.deleteMessage(deleteParams, function(err, data) {
							if (err) 
							{
							      console.log("Delete Error", err);
							} 
							else 
							{
							      console.log("Message Deleted", data);
							}
						      });							      
				
				
				}
			/*
			var deleteParams = {
              QueueUrl: IMAGE_QUEUE_URL,
              ReceiptHandle: data.Messages[0].ReceiptHandle
            };
            	
			sqs.deleteMessage(deleteParams, function(err, data) {
			  if (err) 
			  {
				console.log("Delete Error", err);
			  } 
			  else 
			  {
				console.log("Message Deleted", data);
			  }
			});*/
				
				
				
			});
		loop = loop+1;
		}
});
}



/*
sqs.receiveMessage(params, function(err, data) {
  if (err) {
    console.log("Receive Error", err);
  } else if (data.Messages) {
	  
	  console.log(data.Messages)
    var deleteParams = {
      QueueUrl: VOICE_QUEUE_URL,
      ReceiptHandle: data.Messages[0].ReceiptHandle
    };
    sqs.deleteMessage(deleteParams, function(err, data) {
      if (err) {
        console.log("Delete Error", err);
      } else {
        console.log("Message Deleted", data);
      }
    });
  }
});
*/

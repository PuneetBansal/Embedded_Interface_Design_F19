import boto3

#creating a sqs client for boto3
sqs_client = boto3.client('sqs')

IMAGE_QUEUE ='ImageLabeQueue'
VOICE_QUEUE ='voiceInputQueue'
VOICE_RESPONSE_QUEUE = 'voiceResponseQueue'

IMAGE_QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/998008274670/ImageLabeQueue'
VOICE_QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/998008274670/voiceInputQueue'
VOICE_RESPONSE_URL = 'https://sqs.us-east-1.amazonaws.com/998008274670/voiceResponseQueue'
MY_SQS_QUEUE = 'https://sqs.us-east-1.amazonaws.com/998008274670/EID_PI_Queue'

def sendMessageToSQS(queueURL, messageToSend):
    response = sqs_client.send_message( QueueUrl= queueURL,
                                    MessageBody= messageToSend,
                                    DelaySeconds=5)
    
    print(response['MessageId'])

def createNewQueue(queueName):
    response = sqs_client.create_queue(QueueName= queueName)

def getQueueURL(queueName):
    response = sqs_client.get_queue_url( QueueName=queueName)
    return (response['QueueUrl'])

def getNumberOfMessages(queueURL):
    response = sqs_client.get_queue_attributes(
    QueueUrl=queueURL,
    AttributeNames=['ApproximateNumberOfMessages']
    )
    returnVal = response['Attributes']['ApproximateNumberOfMessages']
    return int(returnVal)
    
def receiveMessageFromQueue(queueURL):
    response = sqs_client.receive_message(
    QueueUrl=queueURL,
    MaxNumberOfMessages=10,
    WaitTimeSeconds= 1)  
    message = response['Messages']
    #for d in message:
    #       print(type(d['Body']))
    return message
    #print (type(message))
    #print(message[3]['Body'])
    #print(response['Messages']['Body'])

#createNewQueue("voiceResponseQueue")
sendMessageToSQS(VOICE_QUEUE_URL,"identify")
sendMessageToSQS(VOICE_QUEUE_URL,"identify1")
sendMessageToSQS(VOICE_RESPONSE_URL,"correcto")
sendMessageToSQS(VOICE_RESPONSE_URL,"correcto1")

#payload = "electronicsCheck"
#sendMessageToSQS(IMAGE_QUEUE_URL,payload)

#number = getNumberOfMessages(IMAGE_QUEUE_URL)
#print(number)

#for i in range(0,number):

#   receiveMessageFromQueue(IMAGE_QUEUE_URL)

#timestamp = '0055' 
#payload = '{ "id": "label", "value": "' + str(timestamp) + ' }'

#createNewQueue('ImageLabeQueue')
#print(getQueueURL('ImageLabeQueue'))
#sendMessageToSQS(payload)
    


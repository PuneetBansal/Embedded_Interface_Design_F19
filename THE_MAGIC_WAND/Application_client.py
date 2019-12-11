'''
Name		:Application_client.py
Author		:Puneet Bansal and Amogh Shrikhande
Reference	:playing audio files in python : https://raspberrypi.stackexchange.com/questions/7088/playing-audio-files-with-python
'''
import boto3
import os 
import vlc
from pygame import mixer
import wave
from sqs import *
from s3 import *

mixer.init()
import RPi.GPIO as GPIO 
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)

#	@param	: photo,bucket
#	@desc	: Function to detect label of the image passed to it.
def detect_labels(photo, bucket):
    name = None
    max_confidence = 0.00
    max_parent = 0  
    client=boto3.client('rekognition')
    response = client.detect_labels(Image={'S3Object':{'Bucket':bucket,'Name':photo}},MaxLabels=10)
    for label in response['Labels']:
        #print('inside for')
        print (label)
        confidence = label['Confidence']
        instance = label['Instances']
        parents = len(label['Parents'])
        #print(type(confidence))
        #(instance != []) and (parents != []):
        if (confidence >= max_confidence):
            max_confidence = label['Confidence']
            name = label['Name']
            max_parent = parents
        #print ("Confidence: " + str(label['Confidence']))
    payload = str(name)
    sendMessageToSQS(IMAGE_QUEUE_URL, payload)
    print('image is ' + name) 
    name = name + " .huh."
    text_to_speech(name)
    return len(response['Labels'])


#	@param	: name
#	@desc	: Function to convert text to speech.
def text_to_speech(name):
    client1=boto3.client('polly')
    response = client1.synthesize_speech(VoiceId='Joanna',
            OutputFormat='mp3', 
            Text = name)

    file = open('speech.mp3', 'wb')
    file.write(response['AudioStream'].read())
    file.close()
    #playsound("/home/pi/EID/project5/speech.mp3")
    mixer.music.load("/home/pi/EID/project5/speech.mp3")
    mixer.music.play()
    while mixer.music.get_busy() == True:
        continue
   

#	@param	: none
#	@desc	: Function that takes audio input from microphone.
def take_voice_input():
    os.system("arecord -D plughw:1,0 -d 3 /home/pi/EID/project5/voiceinput.wav -r 16000 -f S16_LE -t wav")


#	@param	: none
#	@desc	: Function to convert speech to text
def voice_to_text():
    vtotext_client =boto3.client('lex-runtime') 
    take_voice_input()
    fp = wave.open('/home/pi/EID/project5/voiceinput.wav','rb')
    response = vtotext_client.post_content(
        botName = 'Eid_Bot',
        botAlias = 'eid_alias',
        userId = 'myUserId',
        contentType = 'audio/l16; rate=16000;channels=1',
        accept = 'text/plain; charset=utf-8',
        inputStream = fp.readframes(96044)
        )
    print(response)
    sendToQueue= response['inputTranscript']
    #sending the command to sqs queue
    payload = str(sendToQueue)
    if payload in ['identify','correcto','wrongo']:
        sendMessageToSQS(VOICE_QUEUE_URL, payload)
    else:
        sendMessageToSQS(VOICE_QUEUE_URL, 'wrongInput')
    
    print(response['message'])
    return response['message']
    

def main():
    photo='testimage.jpg'
    bucket='eidsuperproject'
    GPIO.setup(11, GPIO.OUT)
    GPIO.output(11,0)
    GPIO.setup(11, GPIO.IN)
    while (1):
        
        if GPIO.input(11) == 1:
            response_from_lex= voice_to_text()        
            if str(response_from_lex) == "Initiating Image Capture":
                print('intiated')
                capture_image()
                label_count=detect_labels(photo, bucket)
                print("Labels detected: " + str(label_count))
            elif str(response_from_lex) == "correcto_response": 
                print('Inside coorecto response')        
                payload = str(response_from_lex)
                sendMessageToSQS(VOICE_RESPONSE_URL, payload)
            elif str(response_from_lex) == "wrongo_response": 
                print('Inside wrongo response')
                payload = str(response_from_lex) 
                sendMessageToSQS(VOICE_RESPONSE_URL, payload)
            count=0;
            for i in range (0,10000):
                count = count+1
            
        #if str(response_from_lex) in ["Initiating Image Capture"]:
        #voice_to_text()
        else: 
            print("Switch Off")
    
if __name__ == "__main__":
    main()
    #downloadImage()

import boto3
import os


#capture the image and upload it to s3 bucket.
def capture_image():
    s3 = boto3.resource('s3')
    os.system("raspistill -o testimage.jpg")
    s3.Object('eidsuperproject','testimage.jpg').upload_file(Filename='/home/pi/EID/project5/testimage.jpg')

#download the image from s3 bucket and store it in the project folder
def downloadImage():
    s3 = boto3.client('s3')
    s3.download_file('eidsuperproject','testimage.jpg','/home/pi/EID/project5/downloadedImage.jpg')

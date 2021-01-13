# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 17:28:25 2020

@author: higor
"""
from datetime import datetime
import cv2
import numpy as np
import time
import requests
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from PIL import Image
import os, os.path
import matplotlib.pyplot as plt
from matplotlib import patches

#Google authorisation
#----------------------
gauth = GoogleAuth()

# Try to load saved client credentials
gauth.LoadCredentialsFile("mycreds.txt")

if gauth.credentials is None:
    # Authenticate via google if they're not there, and get refresh token to automate token retrieval
    gauth.GetFlow()
    gauth.flow.params.update({'access_type': 'offline'})
    gauth.flow.params.update({'approval_prompt': 'force'})
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    gauth.Refresh()
else:
    gauth.Authorize()
    
# Save the current credentials to a file
gauth.SaveCredentialsFile("mycreds.txt")  
drive = GoogleDrive(gauth)
#--------------------

#Face API authorization
#-----------------------
os.environ['FACE_SUBSCRIPTION_KEY'] = 'c03f4bb6a5794c79aa9d6d623b81c30d'
os.environ['FACE_ENDPOINT'] = 'https://iotface1.cognitiveservices.azure.com/'

#Authentication process
subscription_key = os.environ['FACE_SUBSCRIPTION_KEY']
assert subscription_key
face_api_url = os.environ['FACE_ENDPOINT'] + '/face/v1.0/detect'
headers = {'Ocp-Apim-Subscription-Key': subscription_key,
           'Content-Type': 'application/octet-stream'
}
params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
}
#---------------------

#Define number of frames to be captured and interval
watch_time_min = 9 #in minutes
watch_time_sec = 30
interval = 0.991442321 #Target of 1 fps, adjusted for average time taken in for loop
nframes = int(watch_time_min)*1*60 + watch_time_sec
#nframes = 5

#set video capture device
cap = cv2.VideoCapture(0+cv2.CAP_DSHOW)

#Function to rename dictionary keys
#-----------------------
def rename_keys(d, keys):
    return dict([(keys.get(k), v) for k, v in d.items()])
#----------------------


for i in range(nframes):
    # get time now
    now = (datetime.now())
    dt_string = now.strftime("%d-%m-%Y %H-%M-%S")
    dt_string_thingspeak = now.strftime("%d-%m-%Y %H:%M:%S")
    iso8601 = str(dt_string_thingspeak)
    iso8601 = iso8601.replace(" ","T")
    iso8601 = iso8601 + "+00:00"
    
    #capture image
    ret, img = cap.read()
    #time.sleep(1)
    contrast = 1.5
    brightness = 0
    img = np.clip(contrast*img+brightness,0,255)

    # save file jusing current time
    file_dir = './images/'+dt_string+'.jpg'
    cv2.imwrite(file_dir, img)
    
    #run image recognition and upload label to thingspeak
    data = open(file_dir,'rb').read()
    response = requests.post(face_api_url, params=params, headers=headers, data=data)
    faces = response.json()
    print(faces)
    print(type(faces))
    image = Image.open(file_dir)
    plt.figure(figsize=(8,8))
    ax = plt.imshow(image, alpha=1) 
    for face in faces:
        fr = face["faceRectangle"]
        fa = face["faceAttributes"]
        emotions_prob = (fa["emotion"])
        emotion_translations = {   #get emotions as adjective
            'anger':'-5',
            'contempt':'-4', #maps to angry; contempt is shown when angry and the deepface model has no contempt key
            'disgust':'-3',
            'fear':'-2',
            'sadness':'-1',
            'neutral':'0',
            'surprise':'1',
            'happiness':'2'
            }
        emotions_prob = rename_keys(emotions_prob, emotion_translations) #call rename keys function
        
        #find dominant emotion by looking at highest probability emotion
        emotions_prob["0"] = emotions_prob["0"]/100   #calibration to detect more nuances expressions
        emotion = max(emotions_prob, key=emotions_prob.get)
    
        #plot on figure
        origin = (fr["left"], fr["top"])
        p = patches.Rectangle(origin, fr["width"], fr["height"], 
                              fill=False, linewidth=2, color='b')
        ax.axes.add_patch(p)
        plt.text(origin[0], origin[1], "%s, %d"%(emotion, fa["age"]), 
                 fontsize=20, weight="bold", va="bottom", color=("b"))
        plt.axis("off")
        
        writeAPIKey = '' YOUR CHANNEL API KEY IN HERE
        RequestToThingspeak = 'https://api.thingspeak.com/update?api_key='+writeAPIKey+'&field5='+str(emotion)+'&created_at='+str(iso8601)
        requests.get(RequestToThingspeak)    
        time.sleep(5)

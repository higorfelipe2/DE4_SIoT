# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 19:59:22 2020

@author: higor

Posts emotions to thingspeak channel using three loops.
"""


from datetime import datetime
import cv2
import numpy as np
import time
import requests
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import timeit
from PIL import Image
import sys, os, os.path
from matplotlib import patches
import matplotlib.pyplot as plt
from deepface import DeepFace


# =============================================================================
# #Google authorisation - not used for thingspeak posting
# #----------------------
# gauth = GoogleAuth()
# 
# # Try to load saved client credentials
# gauth.LoadCredentialsFile("googlecreds.txt")
# 
# if gauth.credentials is None:
#     # Authenticate via google if they're not there, and get refresh token to automate token retrieval
#     gauth.GetFlow()
#     gauth.flow.params.update({'access_type': 'offline'})
#     gauth.flow.params.update({'approval_prompt': 'force'})
#     gauth.LocalWebserverAuth()
# elif gauth.access_token_expired:
#     gauth.Refresh()
# else:
#     gauth.Authorize()
#     
# # Save the current credentials to a file
# gauth.SaveCredentialsFile("googlecreds.txt")  s
# drive = GoogleDrive(gauth)
# #--------------------
# =============================================================================

def webcam_images_to_local_folders():
    #function that takes webcam image and saves to local folder
    
    #Define number of frames to be captured and interval
    watch_time_min = 30 #in minutes
    watch_time_sec = 0
    #interval = 0.991442321 #Target of 1 fps, adjusted for average time taken in for loop
    nframes = int(watch_time_min)*1*60 + watch_time_sec
    #nframes = 3
    
    #set video capture device
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    
    #capture frames in 1s intervals
    dt_string = []
    now = []
    for i in range(nframes):
        # get time now and capture image, then format date and store
        ret, img = cap.read()
        now.append(datetime.now())
        time.sleep(1)
        dt_string.append(now[i].strftime("%d-%m-%Y %H.%M.%S"))
        contrast = 1.5
        brightness = 0
        img = np.clip(contrast*img+brightness,0,255)

        # save file jusing current time
        cv2.imwrite('./images/'+dt_string[i]+'.jpg', img)
    
    file_dirs = [0]*nframes
    datetimes = [0]*nframes
    for i in range(nframes):    
        file_name = dt_string[i]
        file_dirs[i] = './images/'+dt_string[i]+'.jpg'
        datetimes[i] = dt_string[i]
        
        # wait interval
        stop = timeit.default_timer()
        
        #if period>interval:
            #    interval = (1-((period)-1))
            #else: 
                #    interval = (1+(1-(period)))
        #print('Time: ', stop - start)  
        
        webcam_images_to_local_folders.file_dirs = file_dirs
        webcam_images_to_local_folders.datetimes = datetimes
        webcam_images_to_local_folders.nframes = nframes
    
def emotion_from_local_image_file(images):   
    #function that takes images from local file, runs expression recognition using Azure Face API,
    #and output raw datetime and emotion data

    datetimes = webcam_images_to_local_folders.datetimes
    nframes = webcam_images_to_local_folders.nframes
    emotions = []
    emotions_deepface = []
    
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
    

    #function to rename dictionary keys
    def rename_keys(d, keys):
        return dict([(keys.get(k), v) for k, v in d.items()])
    
    #Deepface for emotion detection -- ended up not using as it was significantly slower than the azure model
    #(time for report: average time = 5.67s)
    def annotate_image_deepface(image_url):
        img = cv2.imread(image_url)
        predictions = DeepFace.analyze(img) #uses FER2013 dataset and others; more accurate than I could get myself
        print(predictions)

    #Azure Face API for emotion detection
    #(time for report: average time = 0.355s)
    def annotate_image(image_url):
        data = open(image_url,'rb').read()
        response = requests.post(face_api_url, params=params, headers=headers, data=data)
        time.sleep(2.8)  # 20 per minute data rate limit on azure face api free
        faces = response.json()
        if isinstance(faces, dict):
            print('dict')
            
        if bool(faces) == True:
            image = Image.open(image_url)
            plt.figure(figsize=(8,8))
            ax = plt.imshow(image, alpha=1)
            for face in faces:
                fr = face["faceRectangle"]
                fa = face["faceAttributes"]
                emotions_prob = (fa["emotion"])
                emotion_translations = {   #get emotions as adjective
                    'anger':-5,
                    'contempt':-4,
                    'disgust':-3,
                    'fear':-2,
                    'sadness':-1,
                    'neutral':0,
                    'surprise':1,
                    'happiness':2
                    }
                emotions_prob = rename_keys(emotions_prob, emotion_translations) #call rename keys function
                
                #find dominant emotion by looking at highest probability emotion
                emotions_prob[0] = emotions_prob[0]/100   #calibration to detect more nuances expressions
                emotion = max(emotions_prob, key=emotions_prob.get)
                emotions.append(emotion)
                
                #plot on figure
                origin = (fr["left"], fr["top"])
                p = patches.Rectangle(origin, fr["width"], fr["height"], 
                                      fill=False, linewidth=2, color='b')
                ax.axes.add_patch(p)
                plt.text(origin[0], origin[1], "%s, %d"%(emotion, fa["age"]), 
                         fontsize=20, weight="bold", va="bottom", color=("b"))
            plt.axis("off")
            
        else:
            emotions.append('') #ensures that emotions list and timestamps list are syncronised
            

    #label images without .jpg and call functions
    for image in images:
        b = os.path.basename(image)               
        if b.endswith('.jpg'):
            b = b[:-4]
            
        start_time_azure = time.time()
        annotate_image(image)
        end_time_azure = time.time()
        print("time for azure model: ")
        print(end_time_azure-start_time_azure)
        
        #----Uncomment to also run deepface model
# =============================================================================
#         start_time_deepface = time.time()
#         annotate_image_deepface(image)
#         end_time_deepface = time.time()
#         print("time for deepface model: ")
#         print(end_time_deepface-start_time_deepface)
# =============================================================================
        
    #concat datetimes with emotions; error handling deals with frames where person may be out of frame -
    #would throw an index error but instead outputs as zero instead
    data_entry = [0]*nframes
    for i in range(len(emotions)):
        #convert timestamp to 8601 format, as needed by thingspeak
        iso8601 = str(datetimes[i])
        iso8601 = iso8601.replace(".",":")
        iso8601 = iso8601.replace(" ","T")
        iso8601 = iso8601 + "+00:00"
        print("emotions i:")
        print(emotions[i])
        print("times i")
        print(iso8601)         
        writeAPIKey = '' YOUR CHANNEL API KEY IN HERE
        #send emotions in list and correspoding timestamp
        RequestToThingspeak = 'https://api.thingspeak.com/update?api_key='+writeAPIKey+'&field1='+str(emotions[i])+'&created_at='+str(iso8601)
        requests.get(RequestToThingspeak)    
        time.sleep(1)
  
            
    emotion_from_local_image_file.data_entry=data_entry

def publish_to_drive(data_entry):
    #function that formats data into correct CSV format, and uploads to google drive as a text file
    #No raw images are actually exported beyond the Azure link, making this more secure
    
    #format data to be in line-by-line csv format
    li = str(data_entry)
    li = li.replace(".",":")
    li = li.replace("[","")
    li = li.replace("]","")
    li = li.replace(", ","\n")
    li = li.replace(";",",")
    li = li.replace("'","")
    

#-------main--------
print("Taking Pictures!")
webcam_images_to_local_folders()
images_dir = webcam_images_to_local_folders.file_dirs
print("Done taking Pictures!")
emotion_from_local_image_file(images_dir)
data_entry = emotion_from_local_image_file.data_entry
#publish_to_drive(data_entry)
#fileNames = publish_to_drive.fileNames
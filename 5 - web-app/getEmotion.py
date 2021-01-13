# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 04:49:51 2021

@author: higor
"""
import requests

#Get emotion from ThingSpeak and convert to string
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def getEmotion():
    CHANNEL_ID = "1279893"
    #READ_API_KEY = "5AYE65MS1DNUDF5V"
    
    call = 'https://api.thingspeak.com/channels/'+CHANNEL_ID+'/fields/2/last.json'
    
    request = requests.get(call).json()
    emonum = request['field2']
    
    emotion = []
    if emonum == "2":
        emotion ="Happy"
    if emonum == "1":
        emotion = "Surprised"
    if emonum == "0":
        emotion = "Neutral"
    if emonum == "-1":
        emotion = "Sad"
    if emonum == "-2":
        emotion = "Scared"
    if emonum == "-3":
        emotion = "Disgusted"
    if emonum == "-4":
        emotion = "Contemptuous"
    if emonum == "-5":
        emotion = "Angry"
    print(emotion)
    return emotion
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == "__main__":
    getEmotion()
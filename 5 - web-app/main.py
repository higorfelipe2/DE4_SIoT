# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 04:03:47 2021

@author: higor
"""

from flask import Flask, render_template, request, flash
from createSpotify import createSpotify
from getEmotion import getEmotion
import spotifyReccy as rec
import os

img_dir = os.path.join('static') #images used in get-emotion-playlist page

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = img_dir
# geo = pygeoip.GeoIP('GeoLiteCity.dat', pygeoip.MEMORY_CACHE)

#rendering the HTML page which has the button

@app.route('/')
@app.route('/welcome')
def welcome():
    full_img_dir = os.path.join(app.config['UPLOAD_FOLDER'],'Mr_Grumpy_GIF.gif')
    return render_template('welcome.html', user_image = full_img_dir)

@app.route('/emotion_playlist')
def emotion_playlist():
    emotion = getEmotion()
    full_img_dir = os.path.join(app.config['UPLOAD_FOLDER'],'Mr_'+emotion+'.png')
    return render_template('emotion-playlist.html', variable = emotion, user_image = full_img_dir)

#background process happening without any refreshing
@app.route('/background_process_test')
def background_process_test():
    print("Hello World")
    createSpotify()
    return "nothing"

@app.route('/')
@app.route('/done')
def done():
    full_img_dir = os.path.join(app.config['UPLOAD_FOLDER'],'Mr_Dash_GIF.gif')
    emotion = getEmotion()
    spotifyObject = createSpotify()
    rec.spotifyReccy(emotion, spotifyObject)
    return render_template('done.html', user_image = full_img_dir)
    

if __name__ == "__main__":
    app.run()
    
    
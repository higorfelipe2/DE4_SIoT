# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 04:24:57 2021

@author: higor
"""
import requests
import json
from spotipy import util
import spotipy

#Create a spotify object with user login details
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def createSpotify():
    ### Spotify Authorization ###
    with open("spotify_credentials.json") as f:
        spotifyCreds = json.load(f)
    username = spotifyCreds['Spotifyusername']   
    token = util.prompt_for_user_token(
        username=spotifyCreds['Spotifyusername'],
        scope=spotifyCreds['Spotifyscope'],
        client_id=spotifyCreds['Spotifyclient_id'],
        client_secret=spotifyCreds['Spotifyclient_secret'],
        redirect_uri=spotifyCreds['Spotifyredirect_uri'])


    
    # Create spotify object with permissions
    spotifyObject = spotipy.Spotify(auth=token)
    print(spotifyObject.recommendation_genre_seeds())

    return spotifyObject
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == "__main__":
    createSpotify()
    

createSpotify()
    
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 12:53:25 2021

@author: higor
"""
import base64
import random
from datetime import date
from createSpotify import createSpotify
from getEmotion import getEmotion

#Make recommended playlist based on emotion
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def spotifyReccy(emotion, spotifyObject):
    
    now = date.today()
    today = now.strftime("%d/%m/%Y")
    
    #spotifyObject = createSpotify()
    
    user_all_data = spotifyObject.current_user()
    user_id = user_all_data["id"]
    print(user_id)#
    
    #Add playlist description and title based on current emotion
    descr = "This is a Spotify playlist made by the 'Mr. Happy Application'. Every track added reflects how "+emotion+" you were at the time it was added!"
    title = "Mr "+emotion+"'s "+emotion+" Songs ("+str(today)+")"
    playlist_all_data = spotifyObject.user_playlist_create(user_id, title, description = descr)
    playlist_id = playlist_all_data["id"]
    
    #Algorithm to get a song list based on emotion; random component added to 
    #each emotion to ensure a new playlist is made every time
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if emotion == "Happy":
        rec = spotifyObject.recommendations(seed_genres=['pop', 'pop-film','k-pop''happy','j-pop'],
                                            target_tempo = 150, target_acousticness = random.uniform(0, 1),
                                            target_danceability = 0.9,target_speechiness = 0.9,
                                            target_loudness = 0.9,target_energy=0.7
                                            )
        
        #Get repective image from file and use as playlist cover image
        encoded = base64.b64encode(open("static/Mr_Happy.png","rb").read())
        spotifyObject.playlist_upload_cover_image(playlist_id,encoded)
        
        #Get list of track URIs for this emotion
        trackURI = []
        for i in range(len(rec['tracks'])):
            #print(i)
            t = rec['tracks'][i]['uri']
            trackURI.append(t)
            
    if emotion == "Surprised":
        rec = spotifyObject.recommendations(seed_genres=['party','punk',''],
                                            target_tempo = 150, target_acousticness = 0.1,
                                            target_liveness = random.uniform(0, 1), target_danceability = 0.9,
                                            target_speechiness = 0.6, target_loudness =0.9,target_energy=0.6,
                                            )
       
        #Get repective image from file and use as playlist cover image
        encoded = base64.b64encode(open("static/Mr_Surprised.png","rb").read())
        spotifyObject.playlist_upload_cover_image(playlist_id,encoded)
        
        #Get list of track URIs for this emotion
        trackURI = []
        for i in range(len(rec['tracks'])):
            #print(i)
            t = rec['tracks'][i]['uri']
            trackURI.append(t)
            
    if emotion == "Neutral":
        rec = spotifyObject.recommendations(seed_genres=['piano','ambient','chill','sleep'],
                                            target_tempo = 100, target_acousticness = 0.4,
                                            target_liveness = 0.4, target_danceability = 0.3,
                                            target_loudness =0.1,target_energy=0.3,
                                            target_instrumentalness = random.uniform(0, 1))
        
        #Get repective image from file and use as playlist cover image
        encoded = base64.b64encode(open("static/Mr_Neutral.png","rb").read())
        spotifyObject.playlist_upload_cover_image(playlist_id,encoded)
        
        #Get list of track URIs for this emotion
        trackURI = []
        for i in range(len(rec['tracks'])):
            #print(i)
            t = rec['tracks'][i]['uri']
            trackURI.append(t)
        
    if emotion == "Sad":
        rec = spotifyObject.recommendations(seed_genres=['sad', 'rainy day','opera','piano'],
                                            target_tempo = 60, target_acousticness = random.uniform(0, 1), target_liveness = 0.1,
                                            target_danceability = 0.1, target_speechiness = 0.2,
                                            target_loudness =0.1,target_energy=0.1, target_instrumentalness=0.3)
        
        #Get repective image from file and use as playlist cover image
        encoded = base64.b64encode(open("static/Mr_Sad.png","rb").read())
        spotifyObject.playlist_upload_cover_image(playlist_id,encoded)
        
        #Get list of track URIs for this emotion
        trackURI = []
        for i in range(len(rec['tracks'])):
            #print(i)
            t = rec['tracks'][i]['uri']
            trackURI.append(t)
            
    if emotion == "Scared":
        rec = spotifyObject.recommendations(seed_genres=['classical','goth'],
                                            target_tempo = 50, target_acousticness = 0.1,
                                            target_liveness = 0.2, target_danceability = 0.1,
                                            target_speechiness = 0.1,target_energy=0.1,
                                            target_instrumentalness = 0.5, target_loudness = random.uniform(0, 1))
        
        #Get repective image from file and use as playlist cover image
        encoded = base64.b64encode(open("static/Mr_Scared.png","rb").read())
        spotifyObject.playlist_upload_cover_image(playlist_id,encoded)
        
        #Get list of track URIs for this emotion
        trackURI = []
        for i in range(len(rec['tracks'])):
            #print(i)
            t = rec['tracks'][i]['uri']
            trackURI.append(t)
        
    if emotion == "Disgusted":
        rec = spotifyObject.recommendations(seed_genres=['honky-tonk', 'new-release'],
                                            target_tempo = 90, target_acousticness = 0.1,
                                            target_liveness = 0.9, target_danceability = 0.1,
                                            target_speechiness = 0.9, target_loudness =random.uniform(0, 1),target_energy=0.6)
                                                 
        #Get repective image from file and use as playlist cover image
        encoded = base64.b64encode(open("static/Mr_Disgusted.png","rb").read())
        spotifyObject.playlist_upload_cover_image(playlist_id,encoded)
        
        #Get list of track URIs for this emotion
        trackURI = []
        for i in range(len(rec['tracks'])):
            #print(i)
            t = rec['tracks'][i]['uri']
            trackURI.append(t)
        
    if emotion == "Contemptuous":
        rec = spotifyObject.recommendations(seed_genres=['work out', 'movies', 'french'],
                                            target_danceability = 0.3,
                                            target_speechiness = 0.2, target_loudness =0.6,target_energy=0.4,
                                            target_instrumentalness = 0.4, target_tempo = random.uniform(0,1))
        
        #Get repective image from file and use as playlist cover image
        encoded = base64.b64encode(open("static/Mr_Contemptuous.png","rb").read())
        spotifyObject.playlist_upload_cover_image(playlist_id,encoded)
        
        #Get list of track URIs for this emotion
        trackURI = []
        for i in range(len(rec['tracks'])):
            #print(i)
            t = rec['tracks'][i]['uri']
            trackURI.append(t)
        
    if emotion == "Angry":
        rec = spotifyObject.recommendations(seed_genres=['metalcore', 'death-metal', 'metal','dubstep'],
                                            target_tempo = 180, target_acousticness = 0.1,
                                            target_danceability = 0.1, target_speechiness = 0.1,
                                            target_loudness=0.9 ,target_energy=0.9,
                                            target_instrumentalness = random.uniform(0, 1))
    
        
        #Get repective image from file and use as playlist cover image
        encoded = base64.b64encode(open("static/Mr_Angry.png","rb").read())
        spotifyObject.playlist_upload_cover_image(playlist_id,encoded)
        
        #Get list of track URIs for this emotion
        trackURI = []
        for i in range(len(rec['tracks'])):
            #print(i)
            t = rec['tracks'][i]['uri']
            trackURI.append(t)
    
    spotifyObject.user_playlist_add_tracks(user_id, playlist_id, trackURI)
    
    return playlist_id
    
if __name__ == "__main__":
    spotifyReccy()

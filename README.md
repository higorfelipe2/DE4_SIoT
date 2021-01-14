# Mr Happy's Mood Playlists
All code necessary to reproduce project, excl. sensitive API and WiFi details. 

<p align="center">Full Project Report
 
<p align="center">App Demo Video


<h2>Data Collection:</h2>

1. Sensor data collected and published to ThingSpeak using [arduino script](https://github.com/higorfelipe2/DE4_SIoT/blob/main/2%20-%20sensor_data_to_thingspeak/Final/sensing-and-publishing-ecg.ino)
2. Emotion data collected and published to ThingSpeak using [python script](https://github.com/higorfelipe2/DE4_SIoT/blob/main/1%20-%20emotions_to_thingspeak/Data%20log%20before%20stream%20(1Hz)/webcam-local_folder-emotions-thingspeak.py)
3. Raw data syncronised using [matlab script](https://github.com/higorfelipe2/DE4_SIoT/blob/main/4%20-%20matlab_neural_net/SyncronizeData.m)
4. Raw and synced data available on [my website](https://www.higoralves.com/mr-happy-app)

<h2>Data Analysis:</h2>

<h3>Neural net</h3>

* Neural Net trained using synced data, called within a [matlab script](https://github.com/higorfelipe2/DE4_SIoT/blob/main/4%20-%20matlab_neural_net/make_neural_net.mlx)

<h3>Timeseries data analysis</h3>

* All analysis available to run, without secret code needed, using [live matlab script](https://github.com/higorfelipe2/DE4_SIoT/blob/main/3%20-%20data_analysis/data_analysis.mlx)


<h2>To Run The App:</h2>

* Run matlab [neural net algorith](https://github.com/higorfelipe2/DE4_SIoT/blob/main/4%20-%20matlab_neural_net/use_neural_net.mlx)
 and [main.py](https://github.com/higorfelipe2/DE4_SIoT/blob/main/5%20-%20web-app/main.py) simutaneoulsy for full app functionality.
The necessary Spotify API auth codes are not included, contact the author for directions.
* Video showing app demo available [on my website](https://www.higoralves.com/mr-happy-app)
 


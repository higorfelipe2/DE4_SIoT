/*
  Author: Higor Alves de Freitas
  Credits:
  - Trevor D. Beydag (https://github.com/trevor-sonic/DWEasyFlipFlop) for DWEasyFlipFlop code
  - 

  Note: Code to publish sensor heart rate data to thingspeak.
*/

//#include "DWEasyFlipFlop.h"
#include "DFRobot_Heartrate.h"
#include "ThingSpeak.h"
#include "secrets.h"
#include <WiFiNINA.h>
#include"secrets.h"
#include <Wire.h>
#define heartratePin A2
#define gsrPin A6

//authorisation for network and thingspeak
char ssid[] = SECRET_SSID;   // your network SSID (name) 
char pass[] = SECRET_PASS;   // your network password
int status = WL_IDLE_STATUS;     // the Wifi radio's status
int keyIndex = 0;            // your network key Index number (needed only for WEP)
WiFiClient  client;
unsigned long myChannelNumber = 1277203;
const char * myWriteAPIKey = "XGCVKVKWC0BC46SX";
DFRobot_Heartrate heartrate(DIGITAL_MODE); ///< ANALOG_MODE or DIGITAL_MODE

int number = 0;
int GSR = A6;
int sensorValue=0;
int gsr_average=0;

void setup() {
  Serial.begin(115200);  // Initialize serial
  
  //WiFi.mode(WIFI_STA); 
  ThingSpeak.begin(client);  // Initialize ThingSpeak
  Serial.println("Hello world!");
  // Connect or reconnect to WiFi
  // attempt to connect to Wifi network:
  while (status != WL_CONNECTED) {
    Serial.print("Attempting to connect to network: ");
    Serial.println(ssid);
    // Connect to WPA/WPA2 network:
    status = WiFi.begin(ssid, pass);

    // wait 10 seconds for connection:
    delay(10000);
}
}

void loop() {  
  uint8_t rateValue;
  int dummy = 2;
  while(dummy < 10){
    long sum =0;
    for(int i=0;i<10;i++){           //Average the 10 measurements to remove the glitc{
        int gsrPin = analogRead(GSR);
        //Serial.println("GSR: ");
        //Serial.println(gsrPin);
        //Serial.println("test2");
        sum += gsrPin;
        delay(5);
        }
    gsr_average = sum/10;
    Serial.println(gsr_average);
    ThingSpeak.setField(3, gsr_average);

    int heartValue = analogRead(heartratePin);
    Serial.println(heartValue);
    ThingSpeak.setField(1, heartValue);
    int x = ThingSpeak.writeFields(myChannelNumber, myWriteAPIKey);
    if(x == 200){
      Serial.println("Channel update successful.");;
    }
    else{
      Serial.println("Problem updating channel. HTTP error code " + String(x));
    }
    delay(500);
   }
}

#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>

ESP8266WiFiMulti WiFiMulti;
double vel=0;
double gyro=0;

void setup() {

  Serial.begin(115200);
  // Serial.setDebugOutput(true);
  pinMode(D8,INPUT);
  Serial.println();
  Serial.println();
  Serial.println();

  for (uint8_t t = 4; t > 0; t--) {
    Serial.printf("[SETUP] WAIT %d...\n", t);
    Serial.flush();
    delay(1000);
  }
  WiFi.mode(WIFI_STA);
  WiFiMulti.addAP("SPACE APPS MEXICALI", "spaceapps19");
}

void loop() {
  // wait for WiFi connection
  if ((WiFiMulti.run() == WL_CONNECTED)) {
    WiFiClient client;
    HTTPClient http;

    gyro=analogRead(A0);
    gyro=map(gyro,0,1024,0,360);
    vel = (digitalRead(D8))? 1: 0;
    String url = "https://440d5657.ngrok.io";
    String value = "?gyro="+String(gyro, DEC);
    value += "&vel=";
    value += String(vel, DEC); 
    url += value;
    Serial.print("[HTTP] begin...\n");
    if (http.begin(client, url)) {  // HTTP

      Serial.print("[HTTP] GET...\n");
      // start connection and send HTTP header
      int httpCode = http.GET();

      // httpCode will be negative on error
      if (httpCode > 0) {
        // HTTP header has been send and Server response header has been handled
        Serial.printf("[HTTP] GET... code: %d\n", httpCode);

        // file found at server
        if (httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_MOVED_PERMANENTLY) {
          String payload = http.getString();
          Serial.println(payload);
        }
      } else {
        Serial.printf("[HTTP] GET... failed, error: %s\n", http.errorToString(httpCode).c_str());
      }

      http.end();
    } else {
      Serial.printf("[HTTP} Unable to connect\n");
    }
  }

  delay(10000);
}

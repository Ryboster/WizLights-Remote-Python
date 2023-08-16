# WizLights-Remote-Python
Control your smart WizLights with an IR receiver.

WARNING: This is a personal project for a highly tailored, personal application. It is NOT the most efficient way to do it; I'm simply compensating for the lack of compatible board.

Hardware:
This repository utilizes 2 seperate boards; Arduino Nano and ESP32.
Arduino nano has a ESP8266 external wifi module (not board), an IR receiver, and 2 LED's connected, whilst the ESP32 only has one LED for communicating receiving of data.

Order of operation:
The nano is awaiting IR data. Once received, it flashes a blue LED. Then it sends it over ESP32's AP to ESP32 board. Once ESP32 receives the IR data, it utilizes
the python script provided to communicate with the lights via the same wifi network the lights are connected to.

ESP32's wifi is working in STA+AP. The AP is used for a more reliable communication with the arduino nano while the Station is used to connect to the same wifi as the lights.
ESP8266 is working in STATION mode alone. It is used to connect to ESP32'S access point.

The red LED on nano is used for communicating erros. Whenever an exception is caught, the LED will start flashing.
The blue LED on nano is used for communicating of receiving of IR data.
The green LED on ESP32 is used for communicating of receiving of IR data via wifi.

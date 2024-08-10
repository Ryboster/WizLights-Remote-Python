# Infrared Controlled Wizlight

### Tested on: 
* E27 Bulb
* ESP32 Board
* VS1838B
* UNO R3 Starter Kit Remote (NEC-16)

### Requirements
* Thonny
* mpremote
* IR Receiver
* IR remote compatible with either of the following encodings: `NEC-8`, `NEC-16`, `SAMSUNG`, `SONY_12`, `SONY_15`, `SONY_20`, `RC5_IR`, `RC6_M0`, `MCE`.<br>


### Install


#### Get requirements
```bash
sudo apt install Thonny
pip install --user mpremote
```

#### Prepare board

1. <b> Flash the board with micropython </b>
There is already a great tutorial on this so I'm going to skip this step. All necessary links are below.
* https://docs.micropython.org/en/latest/esp32/tutorial/intro.html
* https://micropython.org/download/ESP32_GENERIC/


2. <b> Installing ir_rx </b>
Plug your ESP32 in and make sure it's recognized by Thonny. Find out which port the device mounted at, then enter the following command to install the `ir_rx` library. Make sure the device isn't running any loops, otherwise the installation process might be afflicted.
```bash
mpremote connect /dev/XXX mip install github:PeterHinch/micropython_ir/ir_rx
```
<br>

### Load script
Navigate to /esp32 directory and enter the following command to copy `boot.py` file to your ESP32.
```bash
mpremote connect /dev/XXX cp ./boot.py :boot.py
```
<br>

### Connect Light to the ESP32's Access Point
Now making sure your ESP32 is running (blue light will flash), on your phone, connect to the `IoT21` Wi-Fi network with the password `EstIstEinPassword` and navigate to your WiZ app. Next pair your light with the network following instructions on screen.
**Note** that in order to complete the pairing process, you'll need internet access which this network doesn't have. You'll have to switch networks during the pairing process as needed. Otherwise you're gonna get an error and you'll have to restart.
<br>

Once a connection on the light is established, that's it. Adjust your IR decoder and binds, and make sure you run `scan_for_light()` function before sending any commands to the light. This will automatically find the light's IP and save it in the working directory. Note that this has to be done every time you restart the ESP32 as it doesn't support static address allocation.<br>
<br>
https://github.com/peterhinch/micropython_ir/blob/master/RECEIVER.md<br>
<br>

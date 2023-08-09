from pywizlight import wizlight
import time
from vpython import *
import serial

"""
1 Ocean
2 Romance
3 Sunset
4 Party
5 Fireplace
6 Cozy
7 Forest
8 Pastel Colors
9 Wake up
10 Bedtime
11 Warm White
12 Daylight
13 Cool white
14 Night light
15 Focus
16 Relax
17 True colors
18 TV time
19 Plantgrowth
20 Spring
21 Summer
22 Fall
23 Deepdive
24 Jungle
25 Mojito
26 Club
27 Christmas
28 Halloween
"""

class Light_Control:
    def __init__(self):
        self.light = wizlight("192.168.1.239")
        self.brightness = 255
        #self.light.brightness = self.brightness
        print(self.light.scene)
        self.is_on = True

    def on(self):
        self.light.turn_on()
        self.is_on = True
        return

    def off(self):
        self.light.turn_off()
        self.is_on = False
        return

    def cool_white(self):
        self.light.rgb = 255, 255, 255
        self.light.scene = 13
        return

    def night_light(self):
        self.light.scene = 14
        return

    def brightness_up(self):
        if self.brightness == 255 or self.brightness > 255:
            print("MAX Brightness")
            return
        elif self.brightness < 250:
            self.brightness += 5
            self.light.brightness = self.brightness
            print("BRIGHTNESS:",self.brightness)
            return

    def brightness_down(self):
        if self.brightness == 0:
            print("MIN Brightness")
            return
        elif self.brightness > 0:
            self.brightness -= 50
            self.light.brightness = self.brightness
            print("BRIGHTNESS:",self.brightness)
            return


#Light_Control().on()
#x = Light_Control().night_light()

connection = serial.Serial("/dev/ttyUSB0", 9600)
connection.flushInput()
control1 = Light_Control()
while True:
        if connection.in_waiting > 0:
            data = connection.readline().decode('utf-8').strip()
            print(data)
            if data == "6D" or data == "1006D":
                control1.brightness_up()
            elif data == "6E" or data == "1006E":
                control1.brightness_down()
            elif data == "6F" or data == "1006F":
                control1.cool_white()
            elif data == "70" or data == "10070":
                if control1.is_on == False:
                    control1.on()
                elif control1.is_on == True:
                    control1.off()
            time.sleep(0.1)
        time.sleep(0.1)

            #if data.startswith("Received"):
            #    hex_value = data.split()[1]
                #print(hex_value)
        time.sleep(0.1)
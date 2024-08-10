### Execute in micropython
## Blazejowski, G. 2024

# TESTED ON: ESP32

# Wiring:
# VCC - 3.3v
# GND - GND
# S/SIGNAL - GPIO23


import network
import time
from machine import Pin
from ir_rx.nec import NEC_16 # 16 bit NEC decoder

import socket

print("Started")

SSID = 'IoT21'
PASSWORD = 'EstIstEinPassword'
PORT = 38899
SUBNET = "192.168"

class Kek():
    def __init__(self):

        self.LIGHT_IP = "192.168.0.3"
        # Make your light's IP permanent with 
        # echo -n "{\"id\":1,\"method\":\"setPilot\",\"params\":{\"static_ip\":\"192.168.0.5\",\"gateway\":\"192.168.0.1\",\"mask\":\"255.255.255.0\",\"dns1\":\"8.8.8.8\",\"dns2\":\"8.8.4.4\"}}"
        # | nc -u -w 1 192.168.XX.XX 38899


        self.ap = network.WLAN(network.AP_IF)
        self.ap.active(True)
        self.ap.config(essid=SSID, password=PASSWORD, authmode=network.AUTH_WPA2_PSK)
        self.ap.ifconfig(('192.168.0.1', '255.255.255.0', '192.168.4.1', '8.8.8.8'))

        self.ir = NEC_16(Pin(23, Pin.IN), self.callback)

        


        self.LED = Pin(2, Pin.OUT)
        self.light_toggle = False

        print('Access Point set up successfully!')
        print('SSID:', SSID)
        print('IP address:', self.ap.ifconfig()[0])

    
    def send_udp_message(self, ip, port, message):
        addr = (ip, port)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(message, addr) 
        s.close()

    def callback(self, data, addr, ctrl):
        if data < 0:
            print('Repeat code.')
        else:
            print('Data {:02x} Addr {:04x}'.format(data, addr))

        formatted_data = "%02x" % data
        print("data: ", formatted_data)

        if formatted_data == "45" and self.light_toggle:
            print("light OFF")
            self.light_toggle = False
            message = b'{"id":1,"method":"setState","params":{"state":false}}'
            self.send_udp_message(self.LIGHT_IP, PORT, message)

        elif formatted_data == "45" and not self.light_toggle:
            print("light ON")
            self.light_toggle = True
            message = b'{"id":1,"method":"setState","params":{"state":true}}'
            self.send_udp_message(self.LIGHT_IP, PORT, message)

        if formatted_data == '16':
            print("Dimming light")
            message = '{"id":1,"method":"setPilot","params":{"temp":4166,"dimming":10}}'
            self.send_udp_message(self.LIGHT_IP, PORT, message)


        
if __name__ == "__main__":
    running = True
    kek = Kek()

    try:
        while running:
            time.sleep_ms(500)
            kek.LED.value(not kek.LED.value()) 

    except KeyboardInterrupt:
        print("Interrupted! Exiting loop...")
        print("Stopped")

    finally:
        kek.LED.value(0) 
    
# https://www.youtube.com/watch?v=Xch1VZgfH5c
# https://github.com/micropython/micropython/issues/8736
# https://docs.micropython.org/en/latest/reference/mpremote.html
# https://github.com/peterhinch/micropython_ir/blob/master/RECEIVER.md
# https://github.com/BobBaylor/ir_rx
# https://github.com/peterhinch/micropython-samples/blob/master/README.md#5-module-index
# https://docs.sunfounder.com/projects/esp32-starter-kit/en/latest/micropython/basic_projects/py_irremote.html
# The ESP32 is now acting as an access point and ready to accept connections.
# https://seanmcnally.net/wiz-config.html
# https://micropython.org/download/



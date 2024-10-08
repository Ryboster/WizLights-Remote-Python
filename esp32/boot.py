### Execute in micropython
## Blazejowski, G. 2024

# TESTED ON: ESP32

# Wiring:
# VCC - 3.3v
# GND - GND
# S/SIGNAL - GPIO23

import network # For access point setup
import time # For preventing duplicate signals
import socket # For communicating with the light

from machine import Pin # For reading IR signals
from ir_rx.philips import RC6_M0 as decoder # For decoding IR signals


print("Started")

### Access point parameters
SSID = 'IoT21'
PASSWORD = 'EstIstEinPassword'

### Bulb parameters
PORT = 38899
SUBNET_MASK = "192.168.0"


class Interface():
    ''' This class serves as the interface for
        communication between the board and the
        bulb.'''
    
    def __init__(self):
        ''' Access Point setup. '''

        self.LIGHT_IP = None

        self.ap = network.WLAN(network.AP_IF)
        self.ap.active(True)
        self.ap.config(essid=SSID, password=PASSWORD, authmode=network.AUTH_WPA2_PSK)
        self.ap.ifconfig(('192.168.0.1', '255.255.255.0', '192.168.4.1', '8.8.8.8'))

        self.ir = decoder(Pin(23, Pin.IN), self.callback)

        self.LED = Pin(2, Pin.OUT)
        self.light_toggle = False

        print('Access Point set up successfully!')
        print('SSID:', SSID)
        print('IP address:', self.ap.ifconfig()[0])


    def scan_for_light(self):
        ''' This function finds the bulb on the network
            and saves its address for further communication.
            
            NOTE: everytime you restart your ESP32 you'll have
            to call this function in order to populate self.LIGHT_IP
            variable.
        '''
        
        message = b'{"method":"getPilot","params":{}}'
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        while not self.LIGHT_IP:
            for i in range(0, 254):
                addr = (SUBNET_MASK + f".{i}", PORT)
                print("scanning", addr)
                sock.sendto(message, addr)
                sock.settimeout(0.5)
                self.LED.value(not self.LED.value())
                try:
                    data, addr = sock.recvfrom(1024)
                    print(addr)
                    self.LIGHT_IP = str(addr[0])
                    time.sleep_ms(3000)
                    
                    break
                except OSError:
                    self.LIGHT_IP = None

    
    def send_udp_message(self, ip, port, message):   
        ''' Helper function for sending commands to the light.'''
        addr = (ip, port)
        print("sending message to: ", addr)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(message, addr) 
        s.close()

    def callback(self, data, addr, ctrl):
        ''' Callback function for when IR receives a signal.
            Set your binds here.
            '''
        if data < 0:
            print('Repeat code.')
        else:
            print('Data {:02x} Addr {:04x}'.format(data, addr))

        formatted_data = "%02x" % data
        print("data: ", formatted_data)

        if formatted_data == "00" and self.light_toggle:
            print("light OFF")
            self.light_toggle = False
            message = b'{"id":1,"method":"setState","params":{"state":false}}'
            self.send_udp_message(self.LIGHT_IP, PORT, message)
            time.sleep_ms(500)

        elif formatted_data == "00" and not self.light_toggle:
            print("light ON")
            self.light_toggle = True
            message = b'{"id":1,"method":"setState","params":{"state":true}}'
            self.send_udp_message(self.LIGHT_IP, PORT, message)
            message = b'{"id":1,"method":"setPilot","params":{"sceneId":13,"dimming":100}}'
            self.send_udp_message(self.LIGHT_IP, PORT, message)
            time.sleep_ms(500)

        if formatted_data == '01':
            print("Dimming light")
            self.light_toggle = True
            message = '{"id":1,"method":"setPilot","params":{"temp":4166,"dimming":10}}'
            self.send_udp_message(self.LIGHT_IP, PORT, message)
            time.sleep_ms(500)

        if formatted_data == '09':
            self.scan_for_light()


        
if __name__ == "__main__":
    running = True
    driver = Interface()

    try:
        while running:
            time.sleep_ms(500)
            driver.LED.value(not driver.LED.value()) 

    except KeyboardInterrupt:
        print("Interrupted! Exiting loop...")
        print("Stopped")

    finally:
        driver.LED.value(0) 
#include <IRremote.h>

const int blue_led = 3; // blue LED on pin 2
const int red_led = 2; //red LED on pin 3
const int IR_PIN = 7; //IR signal on pin 7

IRrecv irReceiver(IR_PIN);
decode_results irResults;


void flash_red(){
  digitalWrite(red_led, HIGH);
  delay(200);
  digitalWrite(red_led, LOW);
}
void flash_blue() {
  digitalWrite(blue_led, HIGH);
  delay(200);
  digitalWrite(blue_led, LOW);
}

void setup() {
  pinMode(blue_led, OUTPUT);
  pinMode(red_led, OUTPUT);
  Serial.begin(9600);
  irReceiver.enableIRIn();
}

void loop() {
  if (irReceiver.decode(&irResults)) {
    // Print the received IR code to the serial port
    flash_blue();
    Serial.print("Received IR code: 0x");
    Serial.println(irResults.value, HEX);
  
    irReceiver.resume();  // Receive the next IR signal
  
  }}

// Wire Master Reader
// by Nicholas Zambetti <http://www.zambetti.com>

// Demonstrates use of the Wire library
// Reads data from an I2C/TWI slave device
// Refer to the "Wire Slave Sender" example for use with this

// Created 29 March 2006

// This example code is in the public domain.


#include <Wire.h>

void setup() {
  Wire.begin();        // join I2C bus (address optional for master)
  Serial.begin(9600);  // start serial for output
}

void loop() {
  Wire.requestFrom(0, 4);    // request 6 bytes from slave device #8

  while (Wire.available()) { // slave may send less than requested

  byte data[4];
  for(int i = 0; i < 4; i++){
    data[i] = Wire.read();
  }
  int sensorValue1 = (data[1] << 8) | data[0];
  int sensorValue2 = (data[3] << 8) | data[2];

  Serial.print(sensorValue1);
  Serial.print(", ");
  Serial.print(sensorValue2);
  Serial.println(", ");

  }

  delay(100);
}

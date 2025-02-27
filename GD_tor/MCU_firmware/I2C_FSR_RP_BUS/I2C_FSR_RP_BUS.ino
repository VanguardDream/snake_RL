#include <Wire.h>
#include <hardware/timer.h>

// volatile boolean timer1_out = HIGH;
volatile int LED_BRIGHT = 0;
int sensordata[14] = {0};
int sensordata2[14] = {0};
long t_ex = 0;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Wire.begin();
  Serial.begin(115200);

  delay(750);

  startupLED();
}

void loop() {
  unsigned long HZTime = millis();
  for(int idx = 0; idx < 14; idx++){
  Wire.requestFrom(idx, 4); // 슬레이브 주소: 1~14
  unsigned long startTime = millis();
  
  // 타임아웃 설정 (예: 100ms)
  while(Wire.available() < 4 && (millis() - startTime) < 5);

  byte data[4];
  for(int i = 0; i < 4; i++){
    data[i] = Wire.read();
  }
  int sensorValue1 = (data[1] << 8) | data[0];
  int sensorValue2 = (data[3] << 8) | data[2];
  sensordata[idx] = (int16_t) sensorValue1;
  sensordata2[idx] = (int16_t) sensorValue2;
  }

  while(millis() - HZTime < 50);

  for(int i=0; i < (sizeof(sensordata)/sizeof(sensordata[0])); i++){
    // Serial.print(i+1);
    // Serial.print(": ");
    Serial.print(sensordata[i]);
    Serial.print(", ");
    Serial.print(sensordata2[i]);
    Serial.print(", ");
    // Serial.print("|");
  }
  Serial.println("");
  Wire.flush();
}

void loop1(){
  breathingLED();
}

void startupLED() {
  digitalWrite(LED_BUILTIN, HIGH);
  delay(300);
  digitalWrite(LED_BUILTIN, LOW);
  delay(300);
}

void breathingLED() {
  for (int i = 55; i < 256; i++) {
    analogWrite(LED_BUILTIN, i);
    delay(3);
  }
  for (int i = 55; i < 256; i++) {
    analogWrite(LED_BUILTIN, 255 - i);
    delay(3);
  }
  for (int i = 55; i < 256; i++) {
    analogWrite(LED_BUILTIN, i);
    delay(3);
  }
  for (int i = 55; i < 256; i++) {
    analogWrite(LED_BUILTIN, 255 - i);
    delay(3);
  }
  digitalWrite(LED_BUILTIN, LOW);
}
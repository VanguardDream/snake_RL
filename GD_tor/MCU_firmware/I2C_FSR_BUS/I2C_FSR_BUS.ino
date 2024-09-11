#include <Wire.h>

// volatile boolean timer1_out = HIGH;
volatile int LED_BRIGHT = 0;
int sensordata[14] = {0};
int sensordata2[14] = {0};
long t_ex = 0;

// Timer1 interrupt
ISR (TIMER1_COMPA_vect) {
  Serial.write("Timer Test...\n");
}

// Timer3 interrupt
ISR (TIMER3_COMPA_vect) {
  if(LED_BRIGHT <= 10)
  {
    analogWrite(LED_BUILTIN, LED_BRIGHT * 20);
    LED_BRIGHT++;
  }
  else if (LED_BRIGHT > 10 && LED_BRIGHT < 21) {
    analogWrite(LED_BUILTIN, 200 - 20 * (LED_BRIGHT - 10));
    LED_BRIGHT++;
  }
  else {
  LED_BRIGHT = 0;
  }
}

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Wire.begin();
  Serial.begin(115200);

  delay(750);
  setupTimer();
  // setTimer1(1);
  setTimer3(0.05);
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
  sensordata[idx] = sensorValue1;
  sensordata2[idx] = sensorValue2;
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
  // delay(400);
  Wire.flush();
}
void setupTimer() {
  cli();
  // initTimer1();
  initTimer3();
  sei();
}

void initTimer1() {
  TCCR1A = 0;
  TCCR1B = 0;
  TCNT1 = 0;
  OCR1A = 10000;
  TCCR1B = bit(WGM12) | bit(CS12)| bit(CS10);  // WGM12 => CTC(Clear Timer on Compare Match), CS12 & CS10  => prescaler 1/1024
  TIMSK1 = bit(OCIE1A);                        // OCIE1A => Timer1 compare match A interrupt
}

void initTimer3() {
  TCCR3A = 0;
  TCCR3B = 0;
  TCNT3 = 0;
  OCR3A = 10000;
  TCCR3B = bit(WGM32) | bit(CS32);  // WGM32 => CTC(Clear Timer on Compare Match), CS32 => prescaler 1/256
  TIMSK3 = bit(OCIE3A);             // OCIE3A => Timer3 compare match A interrupt
}

void setTimer1(float _time) {
  long cnt = 16000000 / 1024 * _time;  // cnt = clk / prescaler * time(s)
  if(cnt > 65535) {
    cnt = 65535;         // "timer1 16bit counter over."
  }
  OCR1A = cnt;           // Output Compare Register Timer1A
  TIMSK1 = bit(OCIE1A);
}

void setTimer3(float _time) {
  long cnt = 16000000 / 256 * _time;  // cnt = clk / prescaler * time(s)
  if(cnt > 65535) {
    cnt = 65535;        // "timer3 16bit counter over."
  }
  OCR3A = cnt;          // Output Compare Register Timer3A
  TIMSK3 = bit(OCIE3A);
}

void stopTimer1(){
    TIMSK1 = 0;
}

void stopTimer3(){
    TIMSK3 = 0;
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
    delay(2);
  }
  for (int i = 55; i < 256; i++) {
    analogWrite(LED_BUILTIN, 255 - i);
    delay(2);
  }
  for (int i = 55; i < 256; i++) {
    analogWrite(LED_BUILTIN, i);
    delay(2);
  }
  for (int i = 55; i < 256; i++) {
    analogWrite(LED_BUILTIN, 255 - i);
    delay(2);
  }
  digitalWrite(LED_BUILTIN, LOW);
}
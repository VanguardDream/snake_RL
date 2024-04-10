#include <Wire.h>

unsigned char ID = 4;
volatile int LED_TIME = 1;
float alpha = 0.5;
int sensordata = 0;

// Timer1 interrupt
ISR (TIMER1_COMPA_vect) {
  Serial.println(sensordata);
}

// Timer3 interrupt
ISR (TIMER3_COMPA_vect) {
  int tmpdata = analogRead(A0);
  // sensordata = tmpdata;
  sensordata = alpha * tmpdata + (1 - alpha) * sensordata;
}

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Wire.begin(ID-1);
  Serial.begin(9600);

  setupTimer();
  setTimer1(0.1);
  setTimer3(0.01);

  // Wire Callback function
  Wire.onRequest(requestEvent);

  startupLED();
}

void loop() {
  for (int i = 0; i < ID; i++) {
    digitalWrite(LED_BUILTIN, HIGH); // LED 켜기
    delay(200); // 500ms 동안 유지
    digitalWrite(LED_BUILTIN, LOW); // LED 끄기
    delay(100); // 500ms 동안 유지
  }
  delay(400);
}
void setupTimer() {
  cli();
  initTimer1();
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

void requestEvent() {
  Wire.write((byte*)&sensordata, 2);
}
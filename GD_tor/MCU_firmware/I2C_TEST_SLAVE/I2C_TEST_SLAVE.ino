// #include <Wire.h>
#include <BitBang_I2C.h>

// Arbitrary pins I used for testing with an ATmega328p
// Define as -1, -1 to use the Wire library over the default I2C interface
#define SDA_PIN 2
#define SCL_PIN 3
#define BITBANG false

BBI2C bbi2c;
bbi2c.bWire = 0;

const int ledPin = 13; // 내장 LED 핀 (아두이노 우노의 경우 13번 핀)

void setup() {
  // Wire.begin(8); // I2C 주소 8번으로 슬레이브 시작
  // Wire.onReceive(receiveEvent); // 데이터 수신 시 receiveEvent 함수 호출
  pinMode(ledPin, OUTPUT); // LED 핀을 출력 모드로 설정
  Serial.begin(9600); // 시리얼 통신 시작
}

void loop() {
  delay(100); // 무한 루프에서의 불필요한 반복을 방지하기 위해 대기
}

// void receiveEvent(int howMany) {
//   while (Wire.available()) { // 수신된 데이터가 있으면
//     char c = Wire.read(); // 한 바이트씩 읽음
//     Serial.print(c); // 시리얼 모니터에 출력
//   }
//   Serial.println(); // 한 번의 전송이 끝나면 개행

//   digitalWrite(ledPin, HIGH); // LED 켜기
//   delay(100); // LED 켠 상태로 유지
//   digitalWrite(ledPin, LOW); // LED 끄기
// }
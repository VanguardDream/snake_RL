#include <BitBang_I2C.h>

#define SDA_PIN -1
#define SCL_PIN -1
#define BITBANG false

const int ledPin = 13; // 내장 LED 핀 (아두이노 우노의 경우 13번 핀)
BBI2C bbi2c;

void setup() {
  memset(&bbi2c, 0, sizeof(bbi2c));
  bbi2c.bWire = !BITBANG; // use bit bang, not wire library
  bbi2c.iSDA = SDA_PIN;
  bbi2c.iSCL = SCL_PIN;
  I2CInit(&bbi2c, 10000);
  delay(250); // allow devices to power up

  pinMode(ledPin, OUTPUT); // LED 핀을 출력 모드로 설정
  Serial.begin(9600); // 시리얼 통신 시작
}


void loop() {
uint8_t map[16];
char szTemp[32];
uint8_t i;
int iDevice, iCount;
uint32_t u32Caps;

  Serial.println("Starting I2C Scan");
  I2CScan(&bbi2c, map); // get bitmap of connected I2C devices
  if (map[0] == 0xfe) // something is wrong with the I2C bus
  {
    Serial.println("I2C pins are not correct or the bus is being pulled low by a bad device; unable to run scan");
  }
  else
  {
    iCount = 0;
    for (i=1; i<128; i++) // skip address 0 (general call address) since more than 1 device can respond
    {
      if (map[i>>3] & (1 << (i & 7))) // device found
      {
        iCount++;
        Serial.print("Device found at 0x");
        Serial.print(i, HEX);
        iDevice = I2CDiscoverDevice(&bbi2c, i, &u32Caps);
        Serial.print(", type = ");
        I2CGetDeviceName(iDevice, szTemp);
        Serial.print(szTemp); // show the device name as a string
        Serial.print(", capability bits = 0x");
        Serial.println(u32Caps, HEX);
      }
    } // for i
    Serial.print(iCount, DEC);
    Serial.println(" device(s) found");
  }
  delay(5000);
}

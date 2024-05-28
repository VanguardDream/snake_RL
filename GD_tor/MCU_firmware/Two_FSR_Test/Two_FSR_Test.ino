bool blink = false;

void setup() {
    // 초기 설정
    Serial.begin(9600);
}

void loop() {
    int up = analogRead(A0);
    int down = analogRead(A9);
    if (blink) {
        digitalWrite(LED_BUILTIN, HIGH);
    }
    else {
        digitalWrite(LED_BUILTIN, LOW);
    }

    blink = !blink;

    Serial.print("up: ");
    Serial.print(up);
    Serial.print(", down: ");
    Serial.println(down);

    delay(100);
}
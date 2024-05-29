bool blink = false;
unsigned long previousMillis = 0;

// Apply low pass filter to up and down values
static int prevUp = 0;
static int prevDown = 0;

float alpha = 0.6; // Adjust the filter strength (0.0 - 1.0)

void lowPassFilter(int& value, int& prevValue, float alpha) {
    value = alpha * value + (1 - alpha) * prevValue;
    prevValue = value;
}

void setup() {
    // 초기 설정
    Serial.begin(9600);
    pinMode(A3, INPUT);
    pinMode(A2, INPUT);
}

void loop() {
    if (millis() - previousMillis > 200) {
        previousMillis = millis();
        blink = !blink;
        digitalWrite(13, blink);
        // Serial.print("Up: ");
        Serial.print(prevUp);
        Serial.print(",");
        Serial.println(prevDown);
    }

    int up = analogRead(A3);
    int down = analogRead(A2);
    
    lowPassFilter(up, prevUp, alpha);
    lowPassFilter(down, prevDown, alpha);

    delay(10);
}
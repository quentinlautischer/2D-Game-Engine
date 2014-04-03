#include <Arduino.h>

const int HORPIN = 51;
const int VERTPIN = 50;
const int SEL = 5;
const int SPEAK = 6;
const int BUTT_A = 2;
const int BUTT_B = 3;
const int BUTT_C = 4;

void setup() {
    pinMode(BUTT_A, INPUT);
    pinMode(BUTT_B, INPUT);
    pinMode(BUTT_C, INPUT);
    pinMode(SEL, INPUT);
    pinMode(SPEAK, OUTPUT);
    digitalWrite(BUTT_A, HIGH);
    digitalWrite(BUTT_B, HIGH);
    digitalWrite(BUTT_C, HIGH);
    digitalWrite(SEL, HIGH);
    Serial.begin(9600);

}

void loop(){ }


 



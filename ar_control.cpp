#include <Arduino.h>

const int HORPIN = 0; //3
const int VERTPIN = 1; //2
const int SEL = 5;
const int SPEAK = 6;
const int BUTT_A = 2;
const int BUTT_B = 3;
const int BUTT_C = 4;

int offset = 40; // Joystick offset for sensitivity issues
int vert_def = 521; // default vert position
int hor_def = 510; // default horizontal position

void setup() {

    //Pin Inits
    pinMode(BUTT_A, INPUT);
    pinMode(BUTT_B, INPUT);
    pinMode(BUTT_C, INPUT);
    pinMode(SEL, INPUT);
    pinMode(SPEAK, OUTPUT);
    digitalWrite(BUTT_A, HIGH);
    digitalWrite(BUTT_B, HIGH);
    digitalWrite(BUTT_C, HIGH);
    digitalWrite(SEL, HIGH);

    //Universal Joystick Calibration

    int vert_def = analogRead(VERTPIN); // default vert position
    int hor_def = analogRead(HORPIN); // default horizontal position

    Serial.begin(9600);
}

void loop(){ 
    //while(!Serial.available()) { } // Wait until we have a connection, send an arbitary character thrrough

    Serial.read(); // Clear the buffer

    while(1) {

        int curser_vert = analogRead(VERTPIN); // Get the curser vert
        int curser_hor = analogRead(HORPIN); // Get the curser hor

        delay(10); //Reduce Serial send rate, its too fast
        if(digitalRead(BUTT_A) == 0) {Serial.write("A ");} // Pressed A aka attack 1

        if(digitalRead(BUTT_B) == 0) {Serial.write("B ");} // Pressed B aka attack 2

        if((digitalRead(BUTT_C) == 0) && (curser_hor == hor_def) && (curser_vert == vert_def)) {Serial.write("C");} 
        // Pressed C aka sheild but you cant sheild if your moving (can be changed)

        if(curser_vert > (vert_def + offset)){
            Serial.write("D "); // Move down
            Serial.print("D");
        }

        else if(curser_vert < (vert_def - offset)){
            Serial.write("U "); // Move up
            Serial.print("U");
        }

        else{} // Do nothing

        if(curser_hor > (hor_def + offset)){
            Serial.write("R "); // Move right
            Serial.print("R");
        }

        else if(curser_hor < (hor_def - offset)){
            Serial.write("L "); // Move left
            Serial.print("L");
        }

        else{
            Serial.write(" ");
        } // Do nothing
    }
}
 

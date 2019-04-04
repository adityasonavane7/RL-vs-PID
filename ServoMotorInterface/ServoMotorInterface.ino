#include <Servo.h> 
 
Servo myservo;  // create servo object to control a servo  
int pos = 0;    // variable to store the servo position 
int q;
void setup() 
{ 
  Serial.begin(115200);
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object 
} 
 
void loop() 
{ 
  if (Serial.available() > 0){
    q = Serial.parseInt();
    if (q >= 25 && q <= 34){ // Constrain servo between 25 deg and 34 deg 
      myservo.write(q);
    }else if (q <25){
      myservo.write(25);
    }
    else if (q > 34){
      myservo.write(34);
    }
  }
  Serial.println(q);
} 

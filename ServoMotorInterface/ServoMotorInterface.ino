// Sweep
// by BARRAGAN <http://barraganstudio.com> 
// This example code is in the public domain.


#include <Servo.h> 
 
Servo myservo;  // create servo object to control a servo 
                // a maximum of eight servo objects can be created 
 
int pos = 0;    // variable to store the servo position 
 int q;
void setup() 
{ 
  q = 35;
  Serial.begin(115200);
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object 
} 
 
 
void loop() 
{ 
  if (Serial.available() > 0){
    q = Serial.parseInt();
    if (q >= 25 && q <= 34){ 
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

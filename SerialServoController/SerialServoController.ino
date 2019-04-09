#include <Servo.h>
Servo Angler;
int pwm;
boolean ledVal = true;
const int maxAngle = 75;
const int minAngle = 55;
void setup() {
  pinMode(PC13,OUTPUT);
  Serial1.begin(115200);
  // put your setup code here, to run once:
  Angler.attach(PA8);
}

void loop() {
  while (Serial1.available()){
    pwm = Serial1.parseInt();
    digitalWrite(PC13,ledVal);
    (ledVal)?ledVal = false:ledVal = true;
  }
  // put your main code here, to run repeatedly:
  ServoWriter(pwm);
  Serial1.println(pwm);
  delay(1);
}

void ServoWriter(int pwmVal){
  if ((pwmVal <= maxAngle) && (pwmVal >= minAngle)){
    Angler.write(pwmVal);
  }
  else if (pwmVal > maxAngle){
    Angler.write(maxAngle);
  }
  else if (pwmVal < minAngle){
    Angler.write(minAngle);
  }
}

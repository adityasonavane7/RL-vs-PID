  const int trigPin = 3;
  const int echoPin = 2;
  const int trigPin1 = 5;
  const int echoPin1 = 4;
  
  const float Kp = 0.285;
  const float Kd = 0.003;  // defines variables
  long duration;
  int distance,distanceprev;
  int i;
  int q[10];
  #include <Servo.h>
  Servo myServo;
  void setup() {
    myServo.attach(9);
    pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
    pinMode(echoPin, INPUT); // Sets the echoPin as an Input
    
    pinMode(trigPin1, OUTPUT); // Sets the trigPin as an Output
    pinMode(echoPin1, INPUT); // Sets the echoPin as an Input
    Serial.begin(115200); // Starts the serial communication
  }
  
  void loop() {
    digitalWrite(trigPin, LOW);
    // Sets the trigPin on HIGH state for 10 micro seconds
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    // Reads the echoPin, returns the sound wave travel time in microseconds
    duration = pulseIn(echoPin, HIGH,30000);
    // Calculating the distance
    distance = duration*0.034/2;
    if (distance > 50){
      distance = 0;
    }
    float proportional = Kp*(20-distance);
    float derivative = Kd*(distance - distanceprev)/0.005;
    distanceprev = distance;
    float Serval = 28 + proportional + derivative;
    myServo.write(Serval);
    Serial.print(Serval);
    Serial.print(',');
    Serial.println(distance);
    delay(3);
  }

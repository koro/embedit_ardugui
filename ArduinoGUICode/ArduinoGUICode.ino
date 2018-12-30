// intended for use with arduinoGUI.py

#include <Servo.h>

Servo myServo1;
Servo myServo2;

// define pins
byte servoPin1 = 3;
byte servoPin2 = 5;

byte sensorPinVelocity1 = A0;
byte sensorPinVelocity2 = A2;

byte sensorPinAmplitude1 = A1;
byte sensorPinAmplitude2 = A3;

//byte servoMin = 5;
//byte servoMax = 170;

const int timestep = 10;
const float timestepInS = ((float)timestep) / 1000.0;

const float maxAngleSpeed = 360.0; // in deg
const float maxAmplitude = 180.0; // in deg

// values for the oscillators
float pos1 = 0;
float pos2 = 0;

void setup() 
{
  Serial.begin(9600);
  
  // set the start values for both servos to the middle
  myServo1.write(90);
  myServo2.write(90);
  
  // initialize the servo
  myServo1.attach(servoPin1);
  myServo2.attach(servoPin2);
}

// returns a float value in [0,1]
float readFloatValue(int port) {
  return ((float)analogRead(port)) / 1023.;
}

void loop()
{
  { // update the servo 1
    float amplitude = 40.0;
    float velocity = readFloatValue(sensorPinVelocity1) * maxAngleSpeed;
    Serial.println(velocity);
    
    pos1 += velocity * timestepInS;
    int p = (int)(90.0 + sin(pos1 / 180.0 * PI)*amplitude);
    myServo1.write(p);
  }
  
  { // update the servo 2
    float amplitude = 40.0;
    float velocity = readFloatValue(sensorPinVelocity2) * maxAngleSpeed;
    Serial.println(velocity);
    
    pos2 += velocity * timestepInS;
    int p = (int)(90.0 + sin(pos2 / 180.0 * PI)*amplitude);
    myServo2.write(p);
  }
  
  delay(timestep);
}

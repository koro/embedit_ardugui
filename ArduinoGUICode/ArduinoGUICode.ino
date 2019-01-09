// intended for use with arduinoGUI.py

#include <Servo.h>

Servo myServo1;
Servo myServo2;

/*
// PINS (ALPHA)
byte servoPin1 = 4;
byte servoPin2 = 11;

byte sensorPinVelocity = A0;
byte sensorPinAmplitude = A3;
byte sensorPinPhaseOffset = A6;
*/

// PINS (BETA)
byte servoPin1 = 12;
byte servoPin2 = 13;

byte sensorPinVelocity = A0;
byte sensorPinAmplitude = A3;
byte sensorPinPhaseOffset = A5;

//byte servoMin = 5;
//byte servoMax = 170;

const int timestep = 10;
const float timestepInS = ((float)timestep) / 1000.0;

const float maxAngleSpeed = 720.0; // in deg

const float maxAmplitude = 90.0; // in deg

// values for the oscillators
float pos = 0;

void setup() 
{
  analogReference(DEFAULT);
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
  float v = ((float)analogRead(port));
  Serial.print(v);
  Serial.print(" ");
  return v / 1023.;
}

float amplitude = 0;
float velocity = 0;
float offset = 0;

void loop()
{
  amplitude = 0.9*amplitude + 0.1*readFloatValue(sensorPinAmplitude) * maxAmplitude;
  velocity = 0.9*velocity + 0.1*readFloatValue(sensorPinVelocity) * maxAngleSpeed;
  offset = 0.9*offset + 0.1*readFloatValue(sensorPinPhaseOffset);

  // constant drive test
  /*
  amplitude = maxAmplitude;
  velocity = maxAngleSpeed;
  offset = 0;
  */
  
  pos += velocity * timestepInS;
  
  int p1 = (int)(90.0 + sin(pos / 180.0 * PI + offset*PI*0.5)*amplitude);
  myServo1.write(p1);

  //int p1 = (int)(1500.0 + sin(pos / 180.0 * PI + offset*PI*0.5)*amplitude);
  //myServo1.writeMicroseconds(p1);
  
  int p2 = (int)(90.0 + sin(pos / 180.0 * PI - offset*PI*0.5)*amplitude);
  myServo2.write(p2);

  //int p2 = (int)(1500.0 + sin(pos / 180.0 * PI - offset*PI*0.5)*amplitude);
  //myServo2.writeMicroseconds(p2);

  /*
  Serial.print(p1);
  Serial.print(" ");
  Serial.print(p2);
  */

  Serial.println();
  delay(timestep);
}

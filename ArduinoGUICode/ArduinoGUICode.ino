// intended for use with arduinoGUI.py

#include <Servo.h>

Servo myServo1;
Servo myServo2;
byte servoPin1 = 3;
byte servoPin2 = 5;
byte servoMin = 5;
byte servoMax = 170;
byte servoFreq1 = 1;
byte servoFreq2 = 1;
byte servoPhase1 = 0;
byte servoPhase2 = 0;
byte servoAmp1 = 180;
byte servoAmp2 = 180;
byte servoPos1 = 0; // that's the phase
byte servoPos2 = 0;
byte newServoPos1 = servoMin;
byte newServoPos2 = servoMin;
float phase = 0.;

//#define PI 3.141592653589793
long cnt = 0;

//const byte numLEDs = 2;
//byte ledPin[numLEDs] = {12, 13};
//byte ledStatus[numLEDs] = {0, 0};

const byte buffSize = 40;
char inputBuffer[buffSize];
const char startMarker = '<';
const char endMarker = '>';
byte bytesRecvd = 0;
boolean readInProgress = false;
boolean newDataFromPC = false;

char messageFromPC[buffSize] = {0};

unsigned long curMillis;

unsigned long prevReplyToPCmillis = 0;
unsigned long replyToPCinterval = 1000;

//=============

void setup() {
  Serial.begin(57600);
  
//    // flash LEDs so we know we are alive
//  for (byte n = 0; n < numLEDs; n++) {
//     pinMode(ledPin[n], OUTPUT);
//     digitalWrite(ledPin[n], HIGH);
//  }
//  delay(500); // delay() is OK in setup as it only happens once
//  
//  for (byte n = 0; n < numLEDs; n++) {
//     digitalWrite(ledPin[n], LOW);
//  }
  
    // initialize the servo
  myServo1.attach(servoPin1);
  myServo2.attach(servoPin2);
  moveServo();
  
    // tell the PC we are ready
  Serial.println("<Arduino is ready>");
}

//=============

void loop() {
  curMillis = millis();
  getDataFromPC();
  replyToPC();
  // switchLEDs();
  moveServo();
  delay(10);
}

//=============

void getDataFromPC() {

    // receive data from PC and save it into inputBuffer
    
  if(Serial.available() > 0) {

    char x = Serial.read();

      // the order of these IF clauses is significant
      
    if (x == endMarker) {
      readInProgress = false;
      newDataFromPC = true;
      inputBuffer[bytesRecvd] = 0;
      parseData();
    }
    
    if(readInProgress) {
      inputBuffer[bytesRecvd] = x;
      bytesRecvd ++;
      if (bytesRecvd == buffSize) {
        bytesRecvd = buffSize - 1;
      }
    }

    if (x == startMarker) { 
      bytesRecvd = 0; 
      readInProgress = true;
    }
  }
}

//=============
 
void parseData() {

    // split the data into its parts
    // assumes the data will be received as (eg) 0,1,35
    
  char * strtokIndx; // this is used by strtok() as an index
  
  strtokIndx = strtok(inputBuffer,","); // get the first part
  int cmd = atoi(strtokIndx);
  if(cmd == 0) {
    return;
    }
  else {
  
    strtokIndx = strtok(NULL, ","); 
    servoFreq1 = atoi(strtokIndx);
    // ledStatus[0] = atoi(strtokIndx); //  convert to an integer
      
    strtokIndx = strtok(NULL, ","); 
    servoPos1 = atoi(strtokIndx); 
    
    strtokIndx = strtok(NULL, ","); 
    servoAmp1 = atoi(strtokIndx); 
    
    strtokIndx = strtok(NULL, ","); 
    servoFreq2 = atoi(strtokIndx); 
    
    strtokIndx = strtok(NULL, ","); 
    servoPos2 = atoi(strtokIndx); 
  
    strtokIndx = strtok(NULL, ","); 
    servoAmp2 = atoi(strtokIndx); 
  }
}

//=============

void replyToPC() {

   if (newDataFromPC || ((curMillis >> 6)% 100 == 0)) {
    newDataFromPC = false;
//    Serial.print("<LedA ");
//    Serial.print(ledStatus[0]);
//    Serial.print(" LedB ");
//    Serial.print(ledStatus[1]);
    Serial.print("<");
//    Serial.print("<F1 ");
    Serial.print(servoFreq1);
    Serial.print(",");
//    Serial.print(" P1 ");
    Serial.print(servoPos1);
    Serial.print(",");
    Serial.print(servoAmp1);
    Serial.print(",");
//    Serial.print(" F2 ");
    Serial.print(servoFreq2);
    Serial.print(",");
//    Serial.print(" P2 ");
    Serial.print(servoPos2);
    Serial.print(",");
    Serial.print(servoAmp2);
    Serial.print(",");
//    Serial.print(" Time ");
    Serial.print(curMillis >> 9); // divide by 512 is approx = half-seconds
    Serial.println(">");

  }
}

//=============

void moveServo() {
  float po1 = (float(servoPos1) / 180.) * 2. * PI;
  float po2 = (float(servoPos2) / 180.) * 2. * PI;
  float phase1 = (cnt / 100.) * 2. * PI * (servoFreq1 / 45.);
  float phase2 = (cnt / 100.) * 2. * PI * (servoFreq2 / 45.);
  int cp1 = (sin(phase1 + po1) + 1) * (servoAmp1/2); // degrees
  int cp2 = (sin(phase2 + po2) + 1) * (servoAmp2/2); // degrees
//  if (servoPos1 != newServoPos1) {
//    servoPos1 = newServoPos1;
//    myServo1.write(servoPos1);
//  }
  myServo1.write(cp1);
  myServo2.write(cp2);
//  if (servoPos2 != newServoPos2) {
//    servoPos2 = newServoPos2;
//    myServo2.write(servoPos2);
//  }
  cnt += 1;
}

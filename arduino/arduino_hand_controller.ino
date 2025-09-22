
/*
  AK Hand Gesture Arduino Controller - Arduino Code by AHMD
  
  PROJECT DESCRIPTION:
  This Arduino firmware is part of an intelligent gesture control system that enables
  real-time hand gesture recognition and LED control. The system captures hand gestures
  via webcam, processes finger counting using Python/MediaPipe, and sends commands to
  this Arduino sketch via serial communication to control 5 LEDs representing each finger.
  
  FEATURES:
  - Real-time LED control based on finger count (0-5)
  - Special gesture sequences (celebration for 5 fingers, reset for 0)
  - System heartbeat monitoring for reliability
  - Serial communication protocol with validation
  - Modular function architecture for easy expansion
  
  Advanced Arduino sketch for AK hand gesture recognition system
  Controls LEDs based on finger count received from Python system
  
  Hardware Configuration:
  - LEDs on digital pins 2-6 with resistors
  - USB connection for serial communication
  
  Communication Protocol:
  - Baud rate: 9600
  - Receives finger count (0-5) as integer
  
  Author: AK & AHMD
  License: MIT
*/

// AK Hardware Configuration
const int AKLEDS[] = {2, 3, 4, 5, 6};
const int AHMDNUMLEDS = 5;

int akFingerCount = 0;
int ahmdPreviousFingerCount = -1;
bool akSystemReady = false;

void setup() {
  ahmdInitializeSerial();
  akConfigurePins();
  ahmdStartupSequence();
  akSystemReady = true;
  
  Serial.println("AK-AHMD Hand Gesture Controller Ready!");
}

void loop() {
  if (Serial.available() > 0) {
    akFingerCount = Serial.parseInt();
    
    if (ahmdValidateFingerCount(akFingerCount)) {
      if (akFingerCount != ahmdPreviousFingerCount) {
        ahmdUpdateLedDisplay(akFingerCount);
        akLogFingerCount(akFingerCount);
        ahmdPreviousFingerCount = akFingerCount;
        
        akHandleSpecialGestures(akFingerCount);
      }
    }
  }
  
  ahmdSystemHeartbeat();
}

void ahmdInitializeSerial() {
  Serial.begin(9600);
  delay(100);
}

void akConfigurePins() {
  for (int i = 0; i < AHMDNUMLEDS; i++) {
    pinMode(AKLEDS[i], OUTPUT);
    digitalWrite(AKLEDS[i], LOW);
  }
  
  pinMode(LED_BUILTIN, OUTPUT);
}

bool ahmdValidateFingerCount(int count) {
  return (count >= 0 && count <= 5);
}

void ahmdUpdateLedDisplay(int count) {
  akClearAllLeds();
  
  for (int i = 0; i < count && i < AHMDNUMLEDS; i++) {
    digitalWrite(AKLEDS[i], HIGH);
  }
  
  ahmdActivityIndicator();
}

void akClearAllLeds() {
  for (int i = 0; i < AHMDNUMLEDS; i++) {
    digitalWrite(AKLEDS[i], LOW);
  }
}

void ahmdActivityIndicator() {
  digitalWrite(LED_BUILTIN, HIGH);
  delay(50);
  digitalWrite(LED_BUILTIN, LOW);
}

void akLogFingerCount(int count) {
  Serial.print("AK Finger count: ");
  Serial.println(count);
}

void ahmdStartupSequence() {
  Serial.println("AHMD Initializing...");
  
  for (int i = 0; i < AHMDNUMLEDS; i++) {
    digitalWrite(AKLEDS[i], HIGH);
    delay(100);
  }
  
  delay(200);
  
  for (int i = 0; i < AHMDNUMLEDS; i++) {
    digitalWrite(AKLEDS[i], LOW);
    delay(100);
  }
  
  Serial.println("AK System Ready!");
}

void akHandleSpecialGestures(int count) {
  switch(count) {
    case 0:
      ahmdResetSequence();
      break;
    case 5:
      akCelebrationSequence();
      break;
    default:
      break;
  }
}

void akCelebrationSequence() {
  for (int cycle = 0; cycle < 3; cycle++) {
    for (int i = 0; i < AHMDNUMLEDS; i++) {
      digitalWrite(AKLEDS[i], HIGH);
      delay(50);
      digitalWrite(AKLEDS[i], LOW);
    }
  }
  
  ahmdRestoreLedDisplay();
}

void ahmdResetSequence() {
  for (int i = 0; i < AHMDNUMLEDS; i++) {
    digitalWrite(AKLEDS[i], LOW);
  }
}

void ahmdRestoreLedDisplay() {
  ahmdUpdateLedDisplay(akFingerCount);
}

void ahmdSystemHeartbeat() {
  static unsigned long akLastHeartbeat = 0;
  unsigned long currentTime = millis();
  
  if (currentTime - akLastHeartbeat > 5000) {
    if (akSystemReady) {
      digitalWrite(LED_BUILTIN, HIGH);
      delay(10);
      digitalWrite(LED_BUILTIN, LOW);
    }
    akLastHeartbeat = currentTime;
  }
}
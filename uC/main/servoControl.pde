#include <Servo.h>

#define SERVO_SORT_TIMETHRESH 1250
#define SERVO_DISPENSE_TIMETHRESH 500

#define SERVO_SORT_DELAY 750
#define SERVO_SORT_DEFAULT 90
#define SERVO_SORT_GREEN 0
#define SERVO_SORT_RED 180


#define SERVO_SORT_PIN 6
#define SERVO_GREEN_PIN 7
#define SERVO_RED_PIN 8

Servo sortServo;
Servo greenServo;
Servo redServo;

typedef enum {
  sortIdle,
  sortGreen,
  sortRed,
  readDelay
} sortServoState;

sortServoState _servo_sortState = sortIdle;
uint32 _servo_sortStartTime = 0;

void servo_init() {
  greenServo.attach(SERVO_GREEN_PIN);
  sortServo.attach(SERVO_SORT_PIN);
  redServo.attach(SERVO_RED_PIN);

  greenServo.write(75);
  redServo.write(105);
  cmd_registerCallback(0x06, servoGreenDispense_cmd);
  cmd_registerCallback(0x07, servoRedDispense_cmd);  
}

void _servo_sort_periodic() {
  if (_servo_sortState == sortIdle) {
    
    sortServo.write(SERVO_SORT_DEFAULT);

    if(color_isGreenBallPresent()) {
//      SerialUSB.println("Green Ball Present");
      _servo_sortStartTime = millis();
      _servo_sortState = sortGreen;
    } else if (color_isRedBallPresent()) {
//      SerialUSB.println("Red Ball Present");
      _servo_sortStartTime = millis();      
      _servo_sortState = sortRed;
    }
  } else if (_servo_sortState == sortGreen) {
    if (_servo_sortStartTime + SERVO_SORT_TIMETHRESH < millis()) {
//      SerialUSB.println("Green Read Delay");
      _servo_sortState = readDelay; 
      _servo_sortStartTime = millis();
    }else if (_servo_sortStartTime + SERVO_SORT_DELAY < millis()){
//      SerialUSB.println("Green Sort");
      sortServo.write(SERVO_SORT_GREEN);      

    }
  } else if (_servo_sortState == sortRed) {

    if (_servo_sortStartTime + SERVO_SORT_TIMETHRESH < millis()) {
      _servo_sortState = readDelay;
      _servo_sortStartTime = millis();
//      SerialUSB.println("Red Read Delay");      
    }else if (_servo_sortStartTime + SERVO_SORT_DELAY < millis()){
//      SerialUSB.println("Red Back To Idle");
      sortServo.write(SERVO_SORT_RED);      

    }

  }
  else if (_servo_sortState == readDelay) {
    sortServo.write(SERVO_SORT_DEFAULT);
    if ( _servo_sortStartTime + 1000 < millis() ) {
//      SerialUSB.println("Back To Idle");
      _servo_sortState = sortIdle;
    }
  }
  
//  if (getDebug()) {
//    SerialUSB.print(_servo_sortState);
//    SerialUSB.print(",");    
//    SerialUSB.println(_servo_sortStartTime);
//  }
}

typedef enum {
  greenIdle,
  greenDispense
}dispenseGreen;

dispenseGreen greenState = greenIdle;
uint32 dispenseGreenStart = 0;

void servoGreenDispense_cmd(uint8 *buf) {
  if (buf[0] == 2) {
    greenState = greenDispense;
    dispenseGreenStart = millis();
  }
}



void _servo_dispense_green(){
  if (greenState == greenIdle) {
    if (color_isBluePresent()) {

      greenState = greenDispense;
      dispenseGreenStart = millis();
    }
  } else if (greenState == greenDispense) {
    if (millis() < dispenseGreenStart + SERVO_DISPENSE_TIMETHRESH) {
      greenServo.write(135);
    } else {
      greenServo.write(75);
    }
    
    
    if (!color_isBluePresent() && millis() > dispenseGreenStart + SERVO_DISPENSE_TIMETHRESH) {
      greenState = greenIdle;
    }
    
  }
}

typedef enum {
  redIdle,
  redDispense
}dispenseRed;

dispenseRed redState = redIdle;
uint32 dispenseRedStart = 0;

void servoRedDispense_cmd(uint8 *buf) {
  if (buf[0] == 2) {
    redState = redDispense;
    dispenseRedStart = millis();
  }
}



void _servo_dispense_red(){
  if (redState == redIdle) {
    if (color_isBluePresent()) {

      redState = redDispense;
      dispenseRedStart = millis();
    }
  } else if (redState == redDispense) {
    if (millis() < dispenseRedStart + SERVO_DISPENSE_TIMETHRESH) {
      redServo.write(45);
    } else {
      redServo.write(105);
    }
    
    
    if (!color_isBluePresent() && millis() > dispenseRedStart + SERVO_DISPENSE_TIMETHRESH) {
      redState = redIdle;
    }
    
  }
}


void servo_periodic() {
  _servo_sort_periodic();
  _servo_dispense_green();
  _servo_dispense_red();
}

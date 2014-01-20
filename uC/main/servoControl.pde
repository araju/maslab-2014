#include <Servo.h>

#define SERVO_SORT_TIMETHRESH 1250
#define SERVO_DISPENSE_TIMETHRESH 500
#define SERVO_SORT_DELAY 50
Servo sortServo;
Servo greenServo;

typedef enum {
  sortIdle,
  sortGreen,
  sortRed
} sortServoState;

sortServoState _servo_sortState = sortIdle;
uint32 _servo_sortStartTime = 0;

void servo_init() {
  greenServo.attach(7);
  sortServo.attach(8);
  greenServo.write(110);
}

void _servo_sort_periodic() {
  if (_servo_sortState == sortIdle) {
    sortServo.write(90);
    if(color_isGreenBallPresent()) {
      _servo_sortStartTime = millis();
      _servo_sortState = sortGreen;
    } else if (color_isRedBallPresent()) {
      _servo_sortStartTime = millis();      
      _servo_sortState = sortRed;
    }
  } else if (_servo_sortState == sortGreen) {
    if (_servo_sortStartTime + SERVO_SORT_TIMETHRESH < millis()) {
      _servo_sortState = sortIdle; 
    }else if (_servo_sortStartTime + SERVO_SORT_DELAY < millis()){
      sortServo.write(0);      
    }
  } else if (_servo_sortState == sortRed) {

    if (_servo_sortStartTime + SERVO_SORT_TIMETHRESH < millis()) {
      _servo_sortState = sortIdle;      
    }else if (_servo_sortStartTime + SERVO_SORT_DELAY < millis()){
      sortServo.write(1800);      
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
void _servo_dispense_green(){
  if (greenState == greenIdle) {
    if (color_isBluePresent()) {
      SerialUSB.println("Dispense Green");
      greenState = greenDispense;
      dispenseGreenStart = millis();
    }
  } else if (greenState == greenDispense) {
    if (millis() < dispenseGreenStart + SERVO_DISPENSE_TIMETHRESH) {
      greenServo.write(45);
    } else {
      greenServo.write(110);
    }
    
    
    if (!color_isBluePresent() && millis() > dispenseGreenStart + SERVO_DISPENSE_TIMETHRESH) {
      SerialUSB.println("Go Back");
      greenState = greenIdle;
    }
    
  }
}

void servo_periodic() {
  _servo_sort_periodic();
  _servo_dispense_green();
  
}

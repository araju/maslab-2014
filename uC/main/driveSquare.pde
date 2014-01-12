#define straightSpeed 9000
#define turnSpeed 6000
#define straight_ki 5
typedef enum {
  start,
  str1,
  right1,
  str2,
  right2,
  str3,
  right3,
  str4,
  right4,
  done
}driveSquareState;

driveSquareState state = start;
void driveSquare() {
  if (state == start){
    motor_clearTicks();
    state = str1;
  }else if (state == str1) {
    if (driveStraight() == 0) {
          gyro_resetAngle();
          state = right1;
    }
    
  }else if (state == right1) {
    if (turnRight() == 0){
       motor_clearTicks();
       state = str2;
    }
    
  }else if (state == str2) {
    if (driveStraight() == 0) {
          gyro_resetAngle();
          state = right2;
    }
  }else if (state == right2) {
    if (turnRight() == 0){
       motor_clearTicks();
       state = str3;
    }
    
  }else if (state == str3) {
    if (driveStraight() == 0) {
          gyro_resetAngle();
          state = right3;
    }
  }else if (state == right3) {
    if (turnRight() == 0){
       motor_clearTicks();
       state = str4;
    }
    
  }else if (state == str4) {
    if (driveStraight() == 0) {
          gyro_resetAngle();
          state = right4;
    }
  }else if (state == right4) {
    if (turnRight() == 0){
       motor_clearTicks();
       state = done;
    }
    
  }else if (state == done) {
    setMotors(0, 0);
  }
}

int8 driveStraight() { 
  
  int32 leftTicks = motor_getLeftTicks();
  int32 rightTicks = motor_getRightTicks();
  
//  //if the error is negative it means that the right has gone farther than the left
  int32 error = leftTicks - rightTicks;
  
  SerialUSB.println(leftTicks);
  SerialUSB.println(rightTicks);
  SerialUSB.println(error);
  SerialUSB.println("");
  
  setMotors(straightSpeed - error * straight_ki, straightSpeed + error * straight_ki);
//  setMotors(straightSpeed, straightSpeed);
  
  if (((leftTicks + rightTicks) >> 1) > 10000){
    return 0;
  }
  return 1;
}

int8 turnRight() {
  int32 angle =  gyro_getAngle();
  
  setMotors(turnSpeed, -turnSpeed);
  SerialUSB.println("Gyro Angle:");
  SerialUSB.println(angle);
  if (angle > 80000){
   return 0; 
  }
  return 1;
}

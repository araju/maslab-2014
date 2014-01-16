#define squareSize 50 
typedef enum {
  start,
  str1,
  str2,
  str3,
  str4,
  done
}driveSquareState;

driveSquareState state = start;

uint8 getDriveSquareState() {
  return state;
}


void driveSquare() {
  if (state == start) {
    state = str1;
//    motor_setSpeed(540, 0);
    control_setPos(squareSize, 0);
//    control_setTheta(90);
  } else if (state == str1) {

    if (control_getState() == 3) {
//    if (millis() > 10000) {
//      motor_setSpeed(0,0);
//      state = done;
//      control_setTheta(180);
      control_setPos(squareSize, squareSize);
      state = str2;
    }
   
    
  } else if (state == str2) {
    
    if (control_getState() == 3) {
//      control_setTheta(270);
      state = str3;
//      state = done;
      control_setPos(0, squareSize);      
    }
    
  } else if (state == str3) {
    if (control_getState() == 3) {
//      control_setTheta(0);
      control_setPos(0, 0);
      state = str4;
    }
    
  } else if (state == str4) {
    
    if (control_getState() == 3){
//      control_setTheta(180);
      state = done;
    }
  } else if (state == done) {
  }
}

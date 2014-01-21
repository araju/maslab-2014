#define straightSpeed 12000
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
    state = str1;
    sc_drive(100);
//    setMotors(5000, 5000);
  }else if (state == str1) {
    if (millis() > 20000) {
      state = right1;
      sc_turn(90); 
    }
    
  }else if (state == right1) {
    if (millis() > 30000){
       state = str2;
       sc_drive(100);
    }
    
  }else if (state == str2) {
    if (driveStraight() == 0) {
          state = right2;
    }
  }else if (state == right2) {
    if (turnRight() == 0){
       state = str3;
    }
    
  }else if (state == str3) {
    if (driveStraight() == 0) {
          state = right3;
    }
  }else if (state == right3) {
    if (turnRight() == 0){
       state = str4;
    }
    
  }else if (state == str4) {
    if (driveStraight() == 0) {
          state = right4;
    }
  }else if (state == right4) {
    if (turnRight() == 0){
       state = done;
    }
    
  }else if (state == done) {
    setMotors(0, 0);
  }
}

int8 driveStraight() { 

  
  
  return 1;
}

int8 turnRight() {

  return 1;
}

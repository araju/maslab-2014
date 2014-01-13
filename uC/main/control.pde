#define CONTROL_NEWTARGET_ANG_ERROR_THRESH 15
#define CONTROL_TURNTOTARGET_ANG_ERROR_THRESH 5
#define CONTROL_GOTOTARGET_DIST_ERROR_THRESH 3
#define CONTROL_TURNTOFINALHEADING_ANG_ERROR_THRESH 3

#define CONTROL_STRAIGHT_KFF 0
#define CONTROL_STRAIGHT_KP 100
#define CONTROL_STRAIGHT_KI .1
#define CONTROL_STRAIGHT_KD 0

#define CONTROL_TURN_KFF 0
#define CONTROL_TURN_KP 2500
#define CONTROL_TURN_KI 1
#define CONTROL_TURN_KD 0


typedef enum {
  NEW_TARGET,
  TURN_TO_TARGET,
  GO_TO_TARGET,
  TURN_TO_FINAL_HEADING,
  DONE
} controlState_t;



float _control_setPointX = 0;
float _control_setPointY = 0;
float _control_setPointTheta = 0;
controlState_t _control_state = DONE;

float _control_driveController_turnIntegral = 0;
float _control_driveController_driveIntegral = 0;

void control_setX(float x) {
  _control_setPointX = x;
  _control_state = NEW_TARGET;
  _control_driveController_turnIntegral = 0;
  _control_driveController_driveIntegral = 0;
}

void control_setY(float y) {
  _control_setPointY = y;
  _control_state = NEW_TARGET;  
  _control_driveController_turnIntegral = 0;
  _control_driveController_driveIntegral = 0;
}

void control_setTheta(float theta) {
  _control_setPointTheta = theta;
  _control_state = NEW_TARGET;
  _control_driveController_turnIntegral = 0;
  _control_driveController_driveIntegral = 0;
}

void _control_driveController(float distErr, float angleErr) {
  int32 leftMotorCommand = 0;
  int32 rightMotorCommand = 0;
  
  //Drive Controller
  //If we're far, let's add a feed forward term
  if (distErr > 10){
    leftMotorCommand += CONTROL_STRAIGHT_KFF;
    rightMotorCommand += CONTROL_STRAIGHT_KFF;    
  }
  
  leftMotorCommand += distErr * CONTROL_STRAIGHT_KP;
  rightMotorCommand += distErr * CONTROL_STRAIGHT_KP;
  
  _control_driveController_driveIntegral += distErr * DT;
  
  leftMotorCommand += _control_driveController_driveIntegral * CONTROL_STRAIGHT_KI;
  rightMotorCommand += _control_driveController_driveIntegral * CONTROL_STRAIGHT_KI;
  
  
  //Angle Controller
  //If the distance error is really low, then we should add the turning feedforward
  //term.
  if (distErr < .1) {
    leftMotorCommand += CONTROL_TURN_KFF * -1 * sign(angleErr);
    rightMotorCommand += CONTROL_TURN_KFF * sign(angleErr);
  }
  
  leftMotorCommand += angleErr * CONTROL_TURN_KP;
  rightMotorCommand += angleErr * CONTROL_TURN_KP;
  
  setMotors(leftMotorCommand, rightMotorCommand);
}

void _control_newTarget(float distErr, float angleErr) {
  if (angleErr > CONTROL_NEWTARGET_ANG_ERROR_THRESH || 
      angleErr < -CONTROL_NEWTARGET_ANG_ERROR_THRESH) {
        
    _control_state = TURN_TO_TARGET;
  } else {
    _control_state = GO_TO_TARGET;
  }
}

void _control_turnToTarget(float distErr, float angleErr) {

  
  if (angleErr < CONTROL_TURNTOTARGET_ANG_ERROR_THRESH && 
      angleErr > -CONTROL_TURNTOTARGET_ANG_ERROR_THRESH) {
      
      _control_driveController(0, angleErr);
        
//    _control_state = GO_TO_TARGET;
      _control_state = DONE;
  }
}

void _control_goToTarget(float distErr, float angleErr) {

  _control_driveController(distErr, angleErr);
  
  if (angleErr > CONTROL_TURNTOTARGET_ANG_ERROR_THRESH) {
    _control_state = TURN_TO_TARGET;
  }
  
  if (distErr < CONTROL_GOTOTARGET_DIST_ERROR_THRESH) {
    if (_control_setPointTheta < 0) {
      _control_state = DONE;
    }else {
      _control_state = TURN_TO_FINAL_HEADING;
    }
  }
  
}

void _control_turnToFinalHeading(float distErr, float angleErr) {
  //Need to recalculate the angleErr to use the setPointTheta
  angleErr = _control_setPointTheta - state_getTheta();
  if (angleErr > 180) {
    angleErr -= 360;
  }else if (angleErr < -180) {
    angleErr += 360;
  }
  

  _control_driveController(0, angleErr);
  
  if (angleErr < CONTROL_TURNTOFINALHEADING_ANG_ERROR_THRESH &&
      angleErr > -CONTROL_TURNTOFINALHEADING_ANG_ERROR_THRESH) {
  
    _control_state = DONE;
  }
  
}

void _control_done() {
  _control_driveController(0,0);
}

void control_periodic() {
  float currX = state_getX();
  float currY = state_getY();
  float currTheta = state_getTheta();
  
  //Calculate Errors
  float distErr = sqrt(pow(_control_setPointX - currX, 2) + pow(_control_setPointY-currY,2));
  float angleErr = radToDeg(atan2(_control_setPointY - currY, _control_setPointX-currX)) - currTheta;
  
  if (angleErr > 180) {
    angleErr -= 360;
  }else if (angleErr < -180) {
    angleErr += 360;
  }

  switch(_control_state) {
    case NEW_TARGET:
      _control_newTarget(distErr, angleErr);
      break;
      
    case TURN_TO_TARGET:
      _control_turnToTarget(distErr, angleErr);
      break;
      
    case GO_TO_TARGET:
      _control_goToTarget(distErr, angleErr);
      break;
      
    case TURN_TO_FINAL_HEADING:
      _control_turnToFinalHeading(distErr, angleErr);
      break;
    
    case DONE:
      _control_done();
      break;
  }
  
  
}

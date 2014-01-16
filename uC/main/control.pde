#define CONTROL_INVALID_DATA_THRESH -1000
#define CONTROL_TURNTOTARGET_EXIT_ANGTHRESH 4
#define CONTROL_TURNTOTARGET_EXIT_SPEEDTHRESH 180

#define CONTROL_NEWTARGET_TURNTHRESHOLD 15
#define CONTROL_GOTOTARGET_ANGLETHRESH 30
#define CONTROL_GOTOTARGET_DONETHRESH 10

#define CONTROL_FASTTURN_KP 10
#define CONTROL_FASTTURN_KI .5
#define CONTROL_FASTTURN_KD -2

#define CONTROL_SLOWTURN_KP 50
#define CONTROL_SLOWTURN_KI .5
#define CONTROL_SLOWTURN_KD -.2

#define CONTROL_DRIVE_KP 6
#define CONTROL_DRIVE_KI 3
#define CONTROL_DRIVE_KD -2

typedef enum {
  NEW_TARGET,
  TURN_TO_TARGET,
  GO_TO_TARGET,
  DONE
} controlState_t;

controlState_t _control_state = DONE;

float _control_xSetPoint = 0;
float _control_ySetPoint = 0;
float _control_thetaSetPoint = 0;

float _control_angleErrInt = 0;
float _control_driveErrInt = 0;

float _control_driveDot = 0;

uint8 control_getState() {
  return _control_state;
}

uint8 _control_validPos() {
  return _control_xSetPoint > CONTROL_INVALID_DATA_THRESH && 
         _control_ySetPoint > CONTROL_INVALID_DATA_THRESH;
}

uint8 _control_validTheta() {
  return _control_thetaSetPoint && CONTROL_INVALID_DATA_THRESH;
}



void control_setPos(float x, float y) {
  _control_xSetPoint = x;
  _control_ySetPoint = y;
  _control_thetaSetPoint = -10000;
  _control_state = NEW_TARGET;
  _control_angleErrInt = 0;
  _control_driveErrInt = 0;
}

void control_setTheta(float theta) {
  _control_thetaSetPoint = theta;
  _control_xSetPoint = -10000;
  _control_ySetPoint = -10000;
  _control_state = TURN_TO_TARGET;
  _control_angleErrInt = 0;
}



float _control_driveController(float distErr, float angleErr) {
  float baseSpeed = 0;
  _control_driveDot = sqrt(pow(state_getXDot(),2) + pow(state_getYDot(),2));
  
  baseSpeed += distErr * CONTROL_DRIVE_KP;
  baseSpeed += _control_driveErrInt * CONTROL_DRIVE_KI;
  baseSpeed += _control_driveDot * CONTROL_DRIVE_KD;
  
  if (!motor_willSaturate(baseSpeed)){
    _control_driveErrInt += distErr * DT_SLOW;
  }
  
  return baseSpeed;
}



float _control_fastTurn(float distErr, float angleErr) {
  (void)distErr;
  float biasCommand = 0;
  
  _control_angleErrInt += angleErr * DT_SLOW;  
  
  if (abs(_control_angleErrInt) > 200) {
    _control_angleErrInt = sign(_control_angleErrInt) * 200;
  }
  
  biasCommand += angleErr * CONTROL_FASTTURN_KP;
  biasCommand += _control_angleErrInt * CONTROL_FASTTURN_KI;
  biasCommand += state_getThetaDot() * CONTROL_FASTTURN_KD;
  
  return biasCommand;
}

float _control_slowTurn(float distErr, float angleErr) {
  (void)distErr;
  float biasCommand = 0;
  
  _control_angleErrInt += angleErr * DT_SLOW;  
  
  biasCommand += angleErr * CONTROL_SLOWTURN_KP;
  biasCommand += _control_angleErrInt * CONTROL_SLOWTURN_KI;
  biasCommand += state_getThetaDot() * CONTROL_SLOWTURN_KD;
  return biasCommand;
  
}


void _control_newTarget(float distErr, float angleErr) {
  if (abs(angleErr) > CONTROL_NEWTARGET_TURNTHRESHOLD) {
    _control_state = TURN_TO_TARGET;
  }else {
    _control_state = GO_TO_TARGET;
  }
}

void _control_turnToTarget(float distErr, float angleErr) {
  float bias = _control_fastTurn(distErr, angleErr);
  
  motor_setSpeed(0, bias);
  
//  if (getDebug()) {
//    SerialUSB.print("_control_turnToTarget");
//    SerialUSB.print(",");
//    SerialUSB.print(millis());
//    SerialUSB.print(",");
//    SerialUSB.print(state_getTheta());
//    SerialUSB.print(",");
//    SerialUSB.print(angleErr);
//    SerialUSB.print(",");
//    SerialUSB.print(_control_angleErrInt);
//    SerialUSB.print(",");    
//    SerialUSB.println(bias);
//  }
  
  if (abs(angleErr) < CONTROL_TURNTOTARGET_EXIT_ANGTHRESH && 
      abs(motor_getLeftThetaDot()) < CONTROL_TURNTOTARGET_EXIT_SPEEDTHRESH && 
      abs(motor_getRightThetaDot()) < CONTROL_TURNTOTARGET_EXIT_SPEEDTHRESH) {
    if (_control_validPos()) {
      _control_state = GO_TO_TARGET;
      _control_angleErrInt = 0;
      _control_driveErrInt = 0;
      
    }else {
      _control_state = DONE;      
    }
  }
}

void _control_goToTarget(float distErr, float angleErr) {
  float baseCommand = _control_driveController(distErr, angleErr);
  
  float biasCommand = 0;
  
  if (distErr > 25) {
    biasCommand = _control_slowTurn(distErr, angleErr);    
  }

  
//  if (getDebug()) {
//    SerialUSB.print("_control_goToTarget");
//    SerialUSB.print(",");
//    SerialUSB.print(millis());
//    SerialUSB.print(",");    
//    SerialUSB.print(distErr);
//    SerialUSB.print(",");
//    SerialUSB.print(angleErr);
//    SerialUSB.print(","); 
//    SerialUSB.print(_control_angleErrInt);
//    SerialUSB.print(","); 
//    SerialUSB.print(baseCommand);
//    SerialUSB.print(",");    
//    SerialUSB.println(biasCommand);
//  }
//  
  motor_setSpeed(baseCommand, biasCommand);
  
  if (abs(distErr) < CONTROL_GOTOTARGET_DONETHRESH && 
      abs(motor_getLeftThetaDot()) < CONTROL_TURNTOTARGET_EXIT_SPEEDTHRESH && 
      abs(motor_getLeftThetaDot()) < CONTROL_TURNTOTARGET_EXIT_SPEEDTHRESH) {
    _control_state = DONE;
  } else if (abs(angleErr) > CONTROL_GOTOTARGET_ANGLETHRESH) {
    _control_state = TURN_TO_TARGET;
    _control_angleErrInt = 0;
    _control_driveErrInt = 0;
  }
}

void _control_done() {
  _control_driveErrInt = 0;
  _control_angleErrInt = 0;
  motor_setSpeed(0,0); 
}

void control_periodic() {
  float currX = state_getX();
  float currY = state_getY();
  float currTheta = state_getTheta();
  
  float distErr = 0;
  float angleErr = 0;
  float setAngle = 0;
  //Calculate Errors
  
  if ((_control_xSetPoint < CONTROL_INVALID_DATA_THRESH || 
      _control_ySetPoint < CONTROL_INVALID_DATA_THRESH) && 
      _control_thetaSetPoint >= 0) {
    setAngle = _control_thetaSetPoint;
    angleErr = _control_thetaSetPoint - currTheta;
    
  }else if (_control_thetaSetPoint < CONTROL_INVALID_DATA_THRESH && 
           _control_xSetPoint > CONTROL_INVALID_DATA_THRESH &&
           _control_ySetPoint > CONTROL_INVALID_DATA_THRESH) {
    
    distErr = sqrt(pow(_control_xSetPoint - currX, 2) + pow(_control_ySetPoint-currY,2));
    setAngle = radToDeg(atan2(_control_ySetPoint - currY, _control_xSetPoint-currX));
    
    if (setAngle < 0) {
      setAngle += 360;
    }
    angleErr = setAngle - currTheta;   
  }
 
  if (angleErr > 180) {
    angleErr -= 360;
  }else if (angleErr < -180) {
    angleErr += 360;
  }
  
  if (abs(angleErr) > 90) { 
    distErr *= -1;
  }

//  if (getDebug()) {
//    SerialUSB.print("control_periodic,");
//    SerialUSB.print(millis());
//    SerialUSB.print(",");
//    SerialUSB.print(currX);
//    SerialUSB.print(",");
//    SerialUSB.print(currY);
//    SerialUSB.print(",");
//    SerialUSB.print(currTheta);
//    SerialUSB.print(",");
//    SerialUSB.print(distErr);
//    SerialUSB.print(",");
//    SerialUSB.print(setAngle);
//    SerialUSB.print(",");
//    SerialUSB.print(angleErr);
//    SerialUSB.print(",");
//    SerialUSB.println(_control_state);
//  }

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
      
    case DONE:
      _control_done();
      break;
  }
  
  
}

//Wheel Base in cm
#define WHEEL_BASE 20.955
#define WHEEL_RADIUS 9.8425/2
#define pi 3.14159

float _state_X = 0;
float _state_Y = 0;
float _state_theta = 0;
float _state_xDot = 0;
float _state_yDot = 0;
float _state_thetaDot = 0;

float state_getX(){
  return _state_X;
}

float state_getY(){
  return _state_Y;
}

float state_getTheta() {
  return _state_theta;
}

float state_getThetaDot() {
  return _state_thetaDot;
}

float state_getYDot() {
  return _state_yDot;
}

float state_getXDot() {
  return _state_xDot;  
}

void stateEstimation_periodic() {
  float motorLeftThetaDot = degToRad(motor_getLeftThetaDot());
  float motorRightThetaDot = degToRad(motor_getRightThetaDot());
  float gyroThetaDot = gyro_getAngularRate();
  
  _state_xDot = WHEEL_RADIUS / 2 * (motorRightThetaDot + motorLeftThetaDot) *
                cos(degToRad(_state_theta));
                
  _state_yDot = WHEEL_RADIUS / 2 * (motorRightThetaDot + motorLeftThetaDot) *
                sin(degToRad(_state_theta));
                
  float encThetaDot = WHEEL_RADIUS/WHEEL_BASE * (motorRightThetaDot - motorLeftThetaDot);
  
  _state_X += _state_xDot * DT_FAST;
  _state_Y += _state_yDot * DT_FAST;

 
//  if (abs(radToDeg(encThetaDot)) > 10 || abs(gyroThetaDot) > 10) {
  if (abs(gyroThetaDot) > 3){
    _state_thetaDot = gyroThetaDot;
    _state_theta += gyroThetaDot * DT_FAST;
  }else {
    _state_thetaDot = encThetaDot;
    _state_theta += radToDeg(encThetaDot) * DT_FAST;
  }
  
  if (_state_theta > 360) {
    _state_theta -= 360; 
  }else if (_state_theta < 0) {
    _state_theta += 360;
  }
  
//  if (getDebug()) {
//    SerialUSB.print("stateEstimation,");
//    SerialUSB.print(millis());
//    SerialUSB.print(",");
//    SerialUSB.print(_state_X);
//    SerialUSB.print(",");
//    SerialUSB.print(_state_Y);
//    SerialUSB.print(",");    
//    SerialUSB.print(_state_theta);    
//    SerialUSB.print(",");    
//    SerialUSB.print(gyroThetaDot);    
//    SerialUSB.print(",");    
//    SerialUSB.println(radToDeg(encThetaDot));        
//  }
}

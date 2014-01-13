//Wheel Base in cm
#define WHEEL_BASE 20.5
#define WHEEL_RADIUS 9.8425/2
#define pi 3.14159

float _state_X = 0;
float _state_Y = 0;
float _state_theta = 0;

float state_getX(){
  return _state_X;
}

float state_getY(){
  return _state_Y;
}

float state_getTheta() {
  return _state_theta;
}

void stateEstimation_periodic() {
  float motorLeftThetaDot = degToRad(motor_getLeftThetaDot());
  float motorRightThetaDot = degToRad(motor_getRightThetaDot());
  float gyroThetaDot = degToRad(gyro_getAngularRate());
  
  float xDot = WHEEL_RADIUS / 2 * (motorRightThetaDot + motorLeftThetaDot) *
                cos(degToRad(_state_theta));
                
  float yDot = WHEEL_RADIUS / 2 * (motorRightThetaDot + motorLeftThetaDot) *
                sin(degToRad(_state_theta));
                
  float encThetaDot = WHEEL_RADIUS/WHEEL_BASE * (motorRightThetaDot - motorLeftThetaDot);
  
  _state_X += xDot * DT;
  _state_Y += yDot * DT;
 
  if (radToDeg(encThetaDot) > 100) {
    _state_theta -= radToDeg(gyroThetaDot) * DT;
  }else {
    _state_theta += radToDeg(encThetaDot) * DT;
  }
  
  if (_state_theta > 360) {
    _state_theta -= 360; 
  }else if (_state_theta < 0) {
    _state_theta += 360;
  }
}

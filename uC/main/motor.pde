#define MOTOR_L_DIR 2
#define MOTOR_L_PWM 1
#define MOTOR_L_GND 0
#define MOTOR_L_TICK 33
#define MOTOR_L_QUAD 34

#define MOTOR_R_DIR 7
#define MOTOR_R_PWM 6
#define MOTOR_R_GND 5
#define MOTOR_R_TICK 35
#define MOTOR_R_QUAD 36

#define MOTOR_MAXBASESPEED 720

#define MOTOR_SPEEDFILTER_ALFA .95

#define MOTOR_BASE_KP 50
#define MOTOR_BASE_KI 15
#define MOTOR_BASE_KD -.1
#define MOTOR_BASE_K 1


#define MOTOR_BIAS_KP 37.5
#define MOTOR_BIAS_KI 15
#define MOTOR_BIAS_KD -.1
#define MOTOR_BIAS_K 1

//#define TICKS_PER_REV (64 * 29.0)
#define TICKS_PER_REV 1920

volatile int32 _motor_leftTicks = 0;
int32 _motor_leftLastTicks = 0;
float _motor_leftThetaDot = 0;
float _motor_leftLastThetaDot = 0;
int32 _motor_leftLastQuadState = 0;
int8 _motor_leftEncDir = 0;

volatile int32 _motor_rightTicks = 0;
int32 _motor_rightLastTicks = 0;
float _motor_rightThetaDot = 0;
int32 _motor_rightLastQuadState = 0;
int8 _motor_rightEncDir = 0;
float _motor_rightLastThetaDot = 0;

void motor_init() {
 pinMode(MOTOR_L_DIR, OUTPUT);
 pinMode(MOTOR_L_PWM, PWM);
 pinMode(MOTOR_L_GND, OUTPUT);
 pinMode(MOTOR_L_TICK, INPUT);
 pinMode(MOTOR_L_QUAD, INPUT);
 
 
 pinMode(MOTOR_R_DIR, OUTPUT);
 pinMode(MOTOR_R_PWM, PWM);
 pinMode(MOTOR_R_GND, OUTPUT);
 pinMode(MOTOR_R_TICK, INPUT);
 pinMode(MOTOR_R_QUAD, INPUT);

 digitalWrite(MOTOR_L_GND, LOW);
 digitalWrite(MOTOR_R_GND, LOW);
 
 setMotors(0, 0);
 
 noInterrupts();
 _motor_leftLastQuadState = digitalRead(MOTOR_L_QUAD);
 _motor_rightLastQuadState = digitalRead(MOTOR_R_QUAD);
 attachInterrupt(MOTOR_R_TICK, motor_rightIRQ, CHANGE);
 attachInterrupt(MOTOR_L_TICK, motor_leftIRQ, CHANGE);
 interrupts();
 
}

void motor_leftIRQ(){
  uint8 tickState = digitalRead(MOTOR_L_TICK);
  uint8 quadState = digitalRead(MOTOR_L_QUAD);
  //Let's check to see if a transition happened on the quadrature pin
  if (quadState != _motor_leftLastQuadState){
    //If it did we can determine if it is leading or lagging
    if (tickState == HIGH) {
      _motor_leftEncDir = -1;
    }else {
      _motor_leftEncDir = 1; 
    }
  }else{
    //If there was no edge on the quadrature pin, we don't know anything about
    //which direction it's going in. 
  }

  _motor_leftTicks += _motor_leftEncDir;
  _motor_leftLastQuadState = quadState;  
}

void motor_rightIRQ(){
  uint8 tickState = digitalRead(MOTOR_R_TICK);
  uint8 quadState = digitalRead(MOTOR_R_QUAD);
  //Let's check to see if a transition happened on the quadrature pin
  if (quadState != _motor_rightLastQuadState){
    //If it did we can determine if it is leading or lagging
    if (tickState == HIGH) {
      _motor_rightEncDir = -1;
    }else {
      _motor_rightEncDir = 1; 
    }
  }else{
    //If there was no edge on the quadrature pin, we don't know anything about
    //which direction it's going in. 
  }

  _motor_rightTicks += _motor_rightEncDir;
  _motor_rightLastQuadState = quadState; 
}

float _motor_baseSpeedSetPoint = 0;
float _motor_baseSpeedIntErr = 0;
float _motor_baseSpeedLast = 0;
float _motor_baseSpeedDot = 0;
float _motor_baseSpeed = 0;
float _motor_baseSpeedError = 0;

int32 _motor_baseSpeedControl() {
  int32 baseCommand = 0;
  
  _motor_baseSpeed = (_motor_rightThetaDot + _motor_leftThetaDot) / 2;
  _motor_baseSpeedError = _motor_baseSpeedSetPoint - _motor_baseSpeed;
  _motor_baseSpeedIntErr += _motor_baseSpeedError * DT_FAST;
  _motor_baseSpeedDot = (_motor_baseSpeed - _motor_baseSpeedLast) * ONE_DT_FAST;
  _motor_baseSpeedLast = _motor_baseSpeed;
  
  baseCommand += _motor_baseSpeedError * MOTOR_BASE_KP;
  baseCommand += _motor_baseSpeedIntErr * MOTOR_BASE_KI;
  baseCommand += _motor_baseSpeedDot * MOTOR_BASE_KD;
  
  return baseCommand;
}

float _motor_bias = 0;
float _motor_biasSetPoint = 0;
float _motor_biasError = 0;
float _motor_biasIntErr = 0;
float _motor_biasDot = 0;
float _motor_biasLast = 0;

int32 _motor_biasControl() {
  int32 biasCommand = 0;
  
  _motor_bias = (_motor_rightThetaDot - _motor_leftThetaDot) / 2;
  _motor_biasError = _motor_biasSetPoint - _motor_bias;
  _motor_biasIntErr += _motor_biasError * DT_FAST;
  _motor_biasDot = (_motor_bias - _motor_biasLast) * ONE_DT_FAST;
  
  biasCommand += _motor_biasError * MOTOR_BIAS_KP;
  biasCommand += _motor_biasIntErr * MOTOR_BIAS_KI;
  biasCommand += _motor_biasDot * MOTOR_BIAS_KD;  

  return biasCommand;
}

void _motor_control() {
  int32 baseCommand = _motor_baseSpeedControl();
  int32 biasCommand = _motor_biasControl();
  
//  if (getDebug()){
//    SerialUSB.print("_motor_control");
//    SerialUSB.print(",");
//    SerialUSB.print(millis());
//    SerialUSB.print(",");
//    SerialUSB.print(_motor_baseSpeed);
//    SerialUSB.print(",");
//    SerialUSB.print(_motor_baseSpeedSetPoint);
//    SerialUSB.print(",");
//    SerialUSB.print(_motor_bias);
//    SerialUSB.print(",");
//    SerialUSB.println(_motor_biasSetPoint);  
//  }
//  
  
  setMotors(baseCommand, biasCommand);  
}


uint8 motor_willSaturate(float baseSpeed) {
  return abs(baseSpeed) > MOTOR_MAXBASESPEED;
}

uint8 motor_setSpeed(float baseSpeed, float bias) {
  uint8 ret = 0;
  if (abs(baseSpeed) > MOTOR_MAXBASESPEED){
    baseSpeed = MOTOR_MAXBASESPEED * sign(baseSpeed);
    ret = 1;
  }
  
  if (abs(baseSpeed) < 15) {
    _motor_baseSpeedIntErr = 0;
    baseSpeed = 0;
  }
  
  if (abs(bias) < 15) {
    _motor_biasIntErr = 0;
    bias = 0;
  }
  
  _motor_baseSpeedSetPoint = baseSpeed * MOTOR_BASE_K;
  _motor_biasSetPoint = bias * MOTOR_BIAS_K;
  
  return ret;
}

void motor_periodic(uint8 drive) {
  _motor_leftLastThetaDot = _motor_leftThetaDot;
  _motor_rightLastThetaDot = _motor_rightThetaDot;
  
//  _motor_leftThetaDot = _motor_leftThetaDot * MOTOR_SPEEDFILTER_ALFA + 
//                        ((_motor_leftTicks - _motor_leftLastTicks) * 
//                        ONE_DT_FAST / TICKS_PER_REV * 360) * 
//                        (1 - MOTOR_SPEEDFILTER_ALFA);
  _motor_leftThetaDot = ((_motor_leftTicks - _motor_leftLastTicks) * 
                        ONE_DT_FAST / TICKS_PER_REV * 360);
  _motor_rightThetaDot = _motor_rightThetaDot * MOTOR_SPEEDFILTER_ALFA +
                        ((_motor_rightTicks - _motor_rightLastTicks) * 
                        ONE_DT_FAST / TICKS_PER_REV * 360) *
                        (1 - MOTOR_SPEEDFILTER_ALFA); 
  
  _motor_leftLastTicks = _motor_leftTicks;
  _motor_rightLastTicks = _motor_rightTicks;
  
  if (getDebug()) {
    SerialUSB.print("Ticks,");
    SerialUSB.print(_motor_leftTicks);
    SerialUSB.print(",");
    SerialUSB.print(_motor_leftLastTicks);
    SerialUSB.print(",");
    SerialUSB.println(_motor_rightTicks);  
    SerialUSB.print(",");
    SerialUSB.print(_motor_rightLastTicks);
    SerialUSB.print(",");
    SerialUSB.print(_motor_leftThetaDot); 
    SerialUSB.print(",");
    SerialUSB.println(_motor_rightThetaDot);   
  }
  
  if (drive) {
    _motor_control();      
  }

}

void motor_clearTicks(){
 _motor_leftTicks = 0;
 _motor_rightTicks = 0; 
}


void setMotors(int32 baseCommand, int32 biasCommand) {
  digitalWrite(MOTOR_L_DIR, calcDir(baseCommand - biasCommand));
  pwmWrite(MOTOR_L_PWM, calcDuty(baseCommand - biasCommand));
  digitalWrite(MOTOR_R_DIR, calcDir(baseCommand + biasCommand));
  pwmWrite(MOTOR_R_PWM, calcDuty(baseCommand + biasCommand));
}

float motor_getLeftThetaDot(){
  return _motor_leftThetaDot;
}

float motor_getRightThetaDot(){
  return _motor_rightThetaDot;
}

uint32 calcDir(int32 duty) {
  return duty < 0 ? 1 : 0;
}

uint32 calcDuty(int32 duty) { 
  return duty < 0 ? -duty : duty;
}


#define MOTOR_L_DIR 28
#define MOTOR_L_PWM 0

#define MOTOR_L_TICK 31
#define MOTOR_L_QUAD 32

#define MOTOR_R_DIR 27
#define MOTOR_R_PWM 1

#define MOTOR_R_TICK 33
#define MOTOR_R_QUAD 34

#define MOTOR_BALL_DIR 23
#define MOTOR_BALL_PWM 2

#define dbgPin 9

volatile int32 _motor_leftTicks = 0;
int32 _motor_leftLastTicks = 0;
float _motor_leftThetaDot = 0;
int32 _motor_leftLastQuadState = 0;
int8 _motor_leftEncDir = 0;

volatile int32 _motor_rightTicks = 0;
int32 _motor_rightLastTicks = 0;
float _motor_rightThetaDot = 0;
int32 _motor_rightLastQuadState = 0;
int8 _motor_rightEncDir = 0;

void motor_init() {
 pinMode(MOTOR_L_DIR, OUTPUT);
 pinMode(MOTOR_L_PWM, PWM);

 pinMode(MOTOR_L_TICK, INPUT);
 pinMode(MOTOR_L_QUAD, INPUT);
 
 
 pinMode(MOTOR_R_DIR, OUTPUT);
 pinMode(MOTOR_R_PWM, PWM);

 pinMode(MOTOR_R_TICK, INPUT);
 pinMode(MOTOR_R_QUAD, INPUT);
 
 pinMode(MOTOR_BALL_DIR, OUTPUT);
 pinMode(MOTOR_BALL_PWM, PWM);

 digitalWrite(MOTOR_BALL_DIR, LOW);
 pwmWrite(MOTOR_BALL_PWM, 12000);
// pwmWrite(MOTOR_BALL_PWM, 0);
 
 pinMode(dbgPin,OUTPUT);
 
 setMotors(0, 0);
// 
 noInterrupts();
 _motor_leftLastQuadState = digitalRead(MOTOR_L_QUAD);
 _motor_rightLastQuadState = digitalRead(MOTOR_R_QUAD);
 attachInterrupt(MOTOR_R_TICK, motor_rightIRQ, CHANGE);
 attachInterrupt(MOTOR_L_TICK, motor_leftIRQ, CHANGE);
 interrupts();
 
}



void motor_leftIRQ(){
  digitalWrite(dbgPin, HIGH);
  uint8 tickState = digitalRead(MOTOR_L_TICK);
  uint8 quadState = digitalRead(MOTOR_L_QUAD);
  //Let's check to see if a transition happened on the quadrature pin
  if (quadState != _motor_leftLastQuadState){
    //If it did we can determine if it is leading or lagging
    if (tickState == LOW) {
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
  digitalWrite(dbgPin, LOW);  
}

void motor_rightIRQ(){
  digitalWrite(dbgPin, HIGH);    
  uint8 tickState = digitalRead(MOTOR_R_TICK);
  uint8 quadState = digitalRead(MOTOR_R_QUAD);
  //Let's check to see if a transition happened on the quadrature pin
  if (quadState != _motor_rightLastQuadState){
    //If it did we can determine if it is leading or lagging
    if (tickState == LOW) {
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
  digitalWrite(dbgPin, LOW);    
}

void motor_clearTicks(){
 _motor_leftTicks = 0;
 _motor_rightTicks = 0; 
}

void setMotors(int32 dutyL, int32 dutyR) {
//  Serial1.print("Set Motors,");
//  Serial1.print(dutyL);
//  Serial1.print(",");
//  Serial1.println(dutyR); 
  digitalWrite(MOTOR_L_DIR, calcDir(dutyL));
  pwmWrite(MOTOR_L_PWM, calcDuty(dutyL));
  digitalWrite(MOTOR_R_DIR, calcDir(dutyR));
  pwmWrite(MOTOR_R_PWM, calcDuty(dutyR));
}

uint32 calcDir(int32 duty) {
  return duty < 0 ? 1 : 0;
}

uint32 calcDuty(int32 duty) { 
  return duty < 0 ? -duty : duty;
}


int32 motor_getLeftTicks() {
  return _motor_leftTicks;
}

int32 motor_getRightTicks() {
  return _motor_rightTicks;
}


#define SC_TURN_KP 0 
#define SC_TURN_KI 0 
#define SC_TURN_KD 0 

#define SC_STRAIGHTBIAS_KP 200
#define SC_STRAIGHTBIAS_KI 25
#define SC_STRAIGHTBIAS_KD 0

#define SC_STRAIGHTSPEED 16000
//#define SC_STRAIGHTSPEED 6000
#define SC_TURNSPEED 15000
#define SC_SMALLANG_TURNSPEED 13000
//#define SC_TURNSPEED 6000

#define WHEEL_PERIMETER 30.5221
#define TICKS_PER_REV (64 * 29.0)

typedef enum {
  stop,
  turn,
  drive,
  customControl
} controlState;

controlState _sc_state;

int32 _sc_turnSpeed = SC_TURNSPEED;

float _sc_angleSetPoint = 0;
float _sc_distSetPoint = 0;
float _sc_angleErrInt = 0;
float _motor_straightBias = 0;
void _sc_stop() {
  _sc_angleErrInt = 0;
  setMotors(0,0);
}

void _sc_turn() {
  if (_sc_angleSetPoint < 0) {
    setMotors(SC_TURNSPEED, -SC_TURNSPEED);
  }else {
    setMotors(-SC_TURNSPEED, SC_TURNSPEED);
  }
  
  if (abs(_sc_angleSetPoint - gyro_getAngle()) < 3) {
    _sc_state = stop;
  }
  
//  if (getDebug()) {
//    Serial1.print("Turn,");
//    Serial1.print(gyro_getAngle());
//    Serial1.print(",");
//    Serial1.println(_sc_angleSetPoint);
//  }
  
}

void _sc_drive() {
  
  int32 avgTicks = (motor_getLeftTicks() + motor_getRightTicks())/2;
  int32 distErr = _sc_distSetPoint - avgTicks;
  float angleErr = -1 * gyro_getAngle() + _motor_straightBias;
  
  if (angleErr > 180) {
    angleErr -= 360;
  }else if (angleErr < -180) {
    angleErr += 360;
  }

  _sc_angleErrInt += angleErr * DT;

  int32 bias = angleErr * SC_STRAIGHTBIAS_KP;
  bias += _sc_angleErrInt * SC_STRAIGHTBIAS_KI;
  
  int32 base = 0;
  
  if (abs(distErr) > 1500) {
    base = sign(distErr) * SC_STRAIGHTSPEED;
  }else {
    base = (distErr / 1500.0) * (SC_STRAIGHTSPEED - 3000) + sign(distErr) * 3000;
  }
  
  uint8 buf[]= {0x17, 0x03, ((base-bias) & 0x80) | 0, abs(base-bias) & 0xFF, (abs(base-bias) >> 8) & 0xFF}; 
  serial_tx(buf,5);

  buf[2] = ((base+bias) & 0x80) | 1 ;
  buf[3] = abs(base+bias) & 0xFF;
  buf[4] = (abs(base+bias) >> 8) & 0xFF; 
  serial_tx(buf,5);
  
  
  setMotors(base - bias, base + bias);

  if (abs(distErr) < 50) {
    _sc_state = stop;
  }
  
}

void sc_drive(float distance, float angleBias) {
  gyro_resetAngle();
  motor_clearTicks();
  _sc_distSetPoint = distance / WHEEL_PERIMETER * TICKS_PER_REV;
  _motor_straightBias = angleBias;
  _sc_state = drive;
  _sc_angleErrInt = 0;
}

void sc_turn(float degree) {
  gyro_resetAngle();
  _sc_state = turn;
  _sc_angleSetPoint = degree;
  _sc_angleErrInt = 0;
  if (abs(_sc_angleSetPoint)  < 30) {
    _sc_turnSpeed = SC_SMALLANG_TURNSPEED;
  }else {
    _sc_turnSpeed = SC_TURNSPEED;
  }

}

void sc_drive_cmd(uint8 *buf){
  
  if (buf[0] == 2) { 
    SerialUSB.println("Got drive Command");
    sc_drive(((int8)buf[1]) * 1.0, (int8)buf[2] * 1.0); 
  }
}

void sc_turn_cmd(uint8 *buf) {

  if (buf[0] == 2) {
    SerialUSB.println("Got turn Command");
    float angle = (((uint8)buf[1]) | ((int8)buf[2]) << 8) * 1.0;
//    Serial1.println(angle);
    sc_turn(angle);
    
  }
}

void sc_custom(int8 leftMotor, int8 rightMotor) {
  _sc_state = customControl;
  int32 leftCustom = leftMotor * SC_STRAIGHTSPEED / 127;
  int32 rightCustom = rightMotor * SC_STRAIGHTSPEED / 127;
  SerialUSB.print("Custom Command L: ");
  SerialUSB.print(leftCustom);
  SerialUSB.print(" R: ");
  SerialUSB.println(rightCustom);
  setMotors(leftCustom, rightCustom);
}

void sc_custom_cmd(uint8 *buf) {
  if (buf[0] == 2) {

    sc_custom(buf[1], buf[2]);
    
  }
}

void sc_init() {
  cmd_registerCallback(0x12, sc_drive_cmd);
  cmd_registerCallback(0x13, sc_turn_cmd);
  cmd_registerCallback(0x18, sc_custom_cmd);
}

void sc_periodic() {

  
  if (getDebug()) {
    int32 heading = gyro_getAngle() * 100;
//    SerialUSB.print("Heading: ");
//    SerialUSB.println(heading);
//    SerialUSB.print(heading & 0xFF,HEX);
//    SerialUSB.print(" ");
//    SerialUSB.println((heading >> 8) & 0xFF,HEX);
    uint8 msg[] = {0x14, 0x02,heading & 0xFF, (heading >> 8) & 0xFF};
    serial_tx(msg, 4);
    
//    SerialUSB.print("L: ");
//    SerialUSB.print(motor_getLeftTicks());
//    SerialUSB.print(" R: ");
//    SerialUSB.println(motor_getRightTicks());
    
    float avgTicks = (motor_getLeftTicks() + motor_getRightTicks())/2;
    avgTicks = avgTicks/TICKS_PER_REV * WHEEL_PERIMETER;
    int32 dist = (int32) avgTicks * 10;
    msg[0] = 0x15;
    msg[2] = dist & 0xFF;
    msg[3] = (dist >> 8) & 0xFF;
    serial_tx(msg, 4);

  }

  
  if (_sc_state == stop) {
    setMotors(0,0);
  } else if (_sc_state == turn) {
    _sc_turn();    
  } else if (_sc_state == drive) {
    _sc_drive();
  } else if (_sc_state == customControl) {
    // The motor command gets set in the init phase, don't need to have an update command.
  }
}

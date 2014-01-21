
#define SC_TURN_KP 0 
#define SC_TURN_KI 0 
#define SC_TURN_KD 0 

#define SC_STRAIGHTBIAS_KP 400
#define SC_STRAIGHTBIAS_KI 50
#define SC_STRAIGHTBIAS_KD 0

#define SC_STRAIGHTSPEED 12000
#define SC_TURNSPEED 6000

#define WHEEL_PERIMETER 30.5221
#define TICKS_PER_REV (64 * 29.0)

typedef enum {
  stop,
  turn,
  drive
} controlState;

controlState _sc_state;

float _sc_angleSetPoint = 0;
float _sc_distSetPoint = 0;
float _sc_angleErrInt = 0;

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
  
  if (getDebug()) {
//    Serial1.print("Turn,");
//    Serial1.print(gyro_getAngle());
//    Serial1.print(",");
//    Serial1.println(_sc_angleSetPoint - gyro_getAngle());
  }
  
}

void _sc_drive() {
  
  int32 avgTicks = (motor_getLeftTicks() + motor_getRightTicks())/2;
  int32 distErr = _sc_distSetPoint - avgTicks;
  float angleErr = -1 * gyro_getAngle();

  _sc_angleErrInt += angleErr * DT;

  int32 bias = angleErr * SC_STRAIGHTBIAS_KP;
  bias = _sc_angleErrInt * SC_STRAIGHTBIAS_KI;
  
  int32 base = 0;
  
  if (abs(distErr) > 1500) {
    base = sign(distErr) * SC_STRAIGHTSPEED;
  }else {
    base = (distErr / 1500.0) * (SC_STRAIGHTSPEED - 3000) + sign(distErr) * 3000;
  }
  
  if (getDebug()) {
//    Serial1.print("Drive,");
//    Serial1.print(motor_getLeftTicks());
//    Serial1.print(",");    
//    Serial1.print(motor_getRightTicks());
//    Serial1.print(",");    
//    Serial1.println(distErr);
  }
  
  setMotors(base - bias, base + bias);

  if (abs(distErr) < 50) {
    _sc_state = stop;
  }
  
}

void sc_drive(float distance) {
  gyro_resetAngle();
  motor_clearTicks();
  _sc_distSetPoint = distance / WHEEL_PERIMETER * TICKS_PER_REV;
  _sc_state = drive;
  _sc_angleErrInt = 0;
}

void sc_turn(float degree) {
  gyro_resetAngle();
  _sc_state = turn;
  _sc_angleSetPoint = degree;
  _sc_angleErrInt = 0;
}

void sc_drive_cmd(uint8 *buf){
  if (buf[0] == 1) { 
    sc_drive(((int8)buf[1]) * 1.0);
  }
}

void sc_turn_cmd(uint8 *buf) {
  if (buf[0] == 1) {
//    Serial1.print("Serial Turn: ");
//    Serial1.println((int8)buf[1]);
    sc_turn(((int8)buf[1]) * 1.0);
  }
}

void sc_init() {
  cmd_registerCallback(0x12, sc_drive_cmd);
  cmd_registerCallback(0x13, sc_turn_cmd);
}

void sc_periodic() {
  int32 heading = gyro_getAngle() * 100;
  uint8 msg[] = {0x14, 0x02,heading & 0xFF, (heading >> 8) & 0xFF};
  serial_tx(msg, 4);
  
  if (getDebug()) {
    float avgTicks = (motor_getLeftTicks() + motor_getRightTicks())/2;
    avgTicks = avgTicks/TICKS_PER_REV * WHEEL_PERIMETER;
    int32 dist = (int32) avgTicks * 10;
    msg[0] = 0x14;
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
  }
}

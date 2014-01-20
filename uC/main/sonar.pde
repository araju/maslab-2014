#define SONAR_ECHO_F 29
#define SONAR_ECHO_L 24
#define SONAR_ECHO_R 26
#define SONAR_ECHO_B 25
#define SONAR_TRIG 14

#define SONAR_TIME_TO_MM .17

void sonar_init() {
  noInterrupts();
  pinMode(SONAR_ECHO_F, INPUT);
  pinMode(SONAR_ECHO_L, INPUT);
  pinMode(SONAR_ECHO_R, INPUT);
  pinMode(SONAR_ECHO_B, INPUT);  
  pinMode(SONAR_TRIG, OUTPUT);
//  
//  attachInterrupt(SONAR_ECHO_F,sonar_isr_f, CHANGE);
//  attachInterrupt(SONAR_ECHO_L,sonar_isr_l, CHANGE);
  attachInterrupt(SONAR_ECHO_R,sonar_isr_r, CHANGE);
//  attachInterrupt(SONAR_ECHO_B,sonar_isr_b, CHANGE);  
  
  interrupts();
}

volatile uint32 _sonar_startTime_F = 0;
volatile uint32 _sonar_dist_F = 0;

volatile uint32 _sonar_startTime_L = 0;
volatile uint32 _sonar_dist_L = 0;

volatile uint32 _sonar_startTime_B = 0;
volatile uint32 _sonar_dist_B = 0;

volatile uint32 _sonar_startTime_R = 0;
volatile uint32 _sonar_dist_R = 0;

void sonar_isr_f(){
  if (digitalRead(SONAR_ECHO_F)){
    _sonar_startTime_F = micros();
  }else{
    _sonar_dist_F = (micros()-_sonar_startTime_F) * SONAR_TIME_TO_MM;
  }
}

void sonar_isr_l(){
  if (digitalRead(SONAR_ECHO_L)){
    _sonar_startTime_L = micros();
  }else{
    _sonar_dist_L = (micros()-_sonar_startTime_L) * SONAR_TIME_TO_MM;
  }
}

void sonar_isr_r(){
  if (digitalRead(SONAR_ECHO_R)){
    _sonar_startTime_R = micros();
  }else{
    _sonar_dist_R = (micros()-_sonar_startTime_R) * SONAR_TIME_TO_MM;
  }
}

void sonar_isr_b(){
  if (digitalRead(SONAR_ECHO_B)){
    _sonar_startTime_B = micros();
  }else{
    _sonar_dist_B = (micros()-_sonar_startTime_B) * SONAR_TIME_TO_MM;
  }
}

uint8 direction = 0;

void sonar_periodic() {
  if (getDebug()) {
    SerialUSB.print("Distance: ");
    SerialUSB.print(_sonar_dist_F);
    SerialUSB.print(",");
    SerialUSB.print(_sonar_dist_L);
    SerialUSB.print(",");
    SerialUSB.print(_sonar_dist_B);
    SerialUSB.print(",");
    SerialUSB.println(_sonar_dist_R);
    
  }
  
  //Detatch Previous Interrupt
//  if (direction == 0) {
//    detachInterrupt(SONAR_ECHO_F);
//    attachInterrupt(SONAR_ECHO_L, sonar_isr_l, CHANGE);
//    direction++;
//  }else if (direction == 1) {
//    detachInterrupt(SONAR_ECHO_L);
//    attachInterrupt(SONAR_ECHO_B, sonar_isr_b, CHANGE);
//    direction++;
//  }else if (direction == 2) {
//    detachInterrupt(SONAR_ECHO_B);
//    attachInterrupt(SONAR_ECHO_R, sonar_isr_r, CHANGE);
//    direction++;
//  }else if (direction == 3) {
//    detachInterrupt(SONAR_ECHO_R);
//    attachInterrupt(SONAR_ECHO_F, sonar_isr_f, CHANGE);
//    direction = 0;
//  }
  
  //Attach New Interrupt
  
  digitalWrite(SONAR_TRIG, HIGH);
  delayMicroseconds(20);
  digitalWrite(SONAR_TRIG, LOW);
}

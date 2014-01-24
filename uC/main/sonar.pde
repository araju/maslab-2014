#define SONAR_ECHO_F 8
//#define SONAR_ECHO_L 24
//#define SONAR_ECHO_FR 8
//#define SONAR_ECHO_BR 5
#define SONAR_TRIG 18

#define SONAR_TIME_TO_MM .17

void sonar_init() {
  noInterrupts();
  pinMode(SONAR_ECHO_F, INPUT);
//  pinMode(SONAR_ECHO_FR, INPUT);
//  pinMode(SONAR_ECHO_BR, INPUT);
//  pinMode(SONAR_ECHO_B, INPUT);  
  pinMode(SONAR_TRIG, OUTPUT);
//  
  attachInterrupt(SONAR_ECHO_F,sonar_isr_f, CHANGE);
//  attachInterrupt(SONAR_ECHO_L,sonar_isr_fr, CHANGE);
//  attachInterrupt(SONAR_ECHO_R,sonar_isr_br, CHANGE);
//  attachInterrupt(SONAR_ECHO_B,sonar_isr_b, CHANGE);  
  
  interrupts();
}

volatile uint32 _sonar_startTime_F = 0;
volatile uint32 _sonar_dist_F = 0;

volatile uint32 _sonar_startTime_FR = 0;
volatile uint32 _sonar_dist_FR = 0;

volatile uint32 _sonar_startTime_BR = 0;
volatile uint32 _sonar_dist_BR = 0;

//volatile uint32 _sonar_startTime_R = 0;
//volatile uint32 _sonar_dist_R = 0;

void sonar_isr_f(){
  if (digitalRead(SONAR_ECHO_F)){
    _sonar_startTime_F = micros();
  }else{
    uint32 reading = (micros()-_sonar_startTime_F) * SONAR_TIME_TO_MM;
//    _sonar_dist_F = micros() - _sonar_startTime_F;
    _sonar_dist_F = reading > 6000 ? _sonar_dist_F : reading;
  }
}

//void sonar_isr_fr(){
//  if (digitalRead(SONAR_ECHO_FR)){
//    _sonar_startTime_FR = micros();
//  }else{
//    uint32 reading = (micros()-_sonar_startTime_FR) * SONAR_TIME_TO_MM;
//    _sonar_dist_FR = micros() - _sonar_startTime_FR;
////    _sonar_dist_FR = reading > 6000 ? _sonar_dist_FR : reading;
//  }
//}
//
//void sonar_isr_br(){
//  if (digitalRead(SONAR_ECHO_BR)){
//    _sonar_startTime_BR = micros();
//  }else{
//     _sonar_dist_BR = micros() - _sonar_startTime_BR;
////    uint32 reading = (micros()-_sonar_startTime_BR) * SONAR_TIME_TO_MM;
////    _sonar_dist_BR = reading > 6000 ? _sonar_dist_BR : reading;
//  }
//}

//void sonar_isr_b(){
//  if (digitalRead(SONAR_ECHO_B)){
//    _sonar_startTime_B = micros();
//  }else{
//    uint32 reading = (micros()-_sonar_startTime_B) * SONAR_TIME_TO_MM;
//    _sonar_dist_B = reading > 6000 ? _sonar_dist_B : reading;
//  }
//}

uint8 direction = 0;

void sonar_periodic() {
  if (getDebug()) {
//    SerialUSB.print("Distance: ");
//    SerialUSB.print(_sonar_dist_F);
//    SerialUSB.print(",");
//    SerialUSB.print(_sonar_dist_L);
//    SerialUSB.print(",");
//    SerialUSB.print(_sonar_dist_B);
//    SerialUSB.print(",");
//    SerialUSB.println(_sonar_dist_R);
    
  }
  
  //Detatch Previous Interrupt
  
//  if (direction == 0) {
//    detachInterrupt(SONAR_ECHO_BR);
//    attachInterrupt(SONAR_ECHO_F, sonar_isr_f, CHANGE);
//
//    direction++;
//    
//  }else if (direction == 1) {
//    detachInterrupt(SONAR_ECHO_F);
//    attachInterrupt(SONAR_ECHO_FR, sonar_isr_fr, CHANGE);
//   
//    direction++;
//  }else if (direction == 2) {
//    detachInterrupt(SONAR_ECHO_FR);
//    attachInterrupt(SONAR_ECHO_BR, sonar_isr_br, CHANGE);
//  
//    direction = 0;
//  }//else if (direction == 3) {
//    detachInterrupt(SONAR_ECHO_R);
//    attachInterrupt(SONAR_ECHO_F, sonar_isr_f, CHANGE);
//    direction = 0;
//  }
  
  //Attach New Interrupt
  
  if (getDebug()) {
    uint8 buf[5] = {0x0b, 0x03, 0x00, 0x00, 0x00};
    
    buf[2] = 0;
    buf[3] = (_sonar_dist_F / 10) & 0xFF;
    buf[4] = ((_sonar_dist_F / 10) >> 8) & 0xFF;
    serial_tx(buf, 5);  
    
//    buf[2] = 1;
//    buf[3] = (_sonar_dist_FR / 10) & 0xFF;
//    buf[4] = ((_sonar_dist_FR / 10) >> 8) & 0xFF;
//    serial_tx(buf, 5);    
//    
//    buf[2] = 2;
//    buf[3] = (_sonar_dist_BR / 10) & 0xFF;
//    buf[4] = ((_sonar_dist_BR / 10) >> 8) & 0xFF;
//    serial_tx(buf, 5);    
//      SerialUSB.print("F: ");
//      SerialUSB.println(_sonar_dist_F);
//      SerialUSB.print(" FR: ");
//      SerialUSB.print(_sonar_dist_FR);
//      SerialUSB.print(" BR: ");
//      SerialUSB.println(_sonar_dist_BR); 
  }
  

  
  digitalWrite(SONAR_TRIG, HIGH);
  delayMicroseconds(20);
  digitalWrite(SONAR_TRIG, LOW);
}

#define SONAR_ECHO 14
//#define SONAR_TRIG 23
#define SONAR_TRIG 9
#define SONAR_GND 8


#define SONAR_TIME_TO_MM .17

void sonar_init() {
  noInterrupts();
  pinMode(SONAR_GND, OUTPUT);
  pinMode(SONAR_ECHO, INPUT);
  pinMode(SONAR_TRIG, OUTPUT);
  
  digitalWrite(SONAR_ECHO,LOW);
  attachInterrupt(SONAR_ECHO,sonar_isr, CHANGE);
  
  interrupts();
}

volatile uint32 _sonar_startTime = 0;
volatile uint32 _sonar_dist = 0;

void sonar_isr(){
  if (digitalRead(SONAR_ECHO)){
    _sonar_startTime = micros();
  }else{
    _sonar_dist = (micros()-_sonar_startTime) * SONAR_TIME_TO_MM;
  }
}

void sonar_periodic() {
//  if (getDebug()) {
//    SerialUSB.print("Distance: ");
//    SerialUSB.println(_sonar_dist);
//  }
  
  digitalWrite(SONAR_TRIG, HIGH);
  delayMicroseconds(20);
  digitalWrite(SONAR_TRIG, LOW);
}

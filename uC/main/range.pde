#define RANGE_FL 24
#define RANGE_FR 37
#define RANGE_BL 36
#define RANGE_BR 35

uint8 _range_fl = 0;
uint8 _range_fr = 0;
uint8 _range_bl = 0;
uint8 _range_br = 0;

void range_init() {
  pinMode(RANGE_FL, INPUT);
  pinMode(RANGE_FR, INPUT);
  pinMode(RANGE_BL, INPUT);
  pinMode(RANGE_BR, INPUT);  
}

void range_periodic() {
  _range_fl = digitalRead(RANGE_FL);
  _range_fr = digitalRead(RANGE_FR);
  _range_bl = digitalRead(RANGE_BL);
  _range_br = digitalRead(RANGE_BR);
  
  if (getDebug()) {
//    SerialUSB.print("FL: ");
//    SerialUSB.print(_range_fl);
//    SerialUSB.print(" FR: ");
//    SerialUSB.print(_range_fr);    
//    SerialUSB.print(" BL: ");
//    SerialUSB.print(_range_bl);    
//    SerialUSB.print(" BR: ");    
//    SerialUSB.println(_range_br);    
  }
}

#define RANGE_FL 24
#define RANGE_FR 37
#define RANGE_BL 36
#define RANGE_BR 35

#define RANGE_DEB_THRESH 10

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

uint8 _range_fl_count = 0;
uint8 _range_fr_count = 0;
uint8 _range_bl_count = 0;
uint8 _range_br_count = 0;

void range_periodic() {
  if (_range_fl != !digitalRead(RANGE_FL)) {
    _range_fl_count++;
    
    if (_range_fl_count > RANGE_DEB_THRESH) {
      _range_fl = !digitalRead(RANGE_FL);
    }
  } else {
    _range_fl_count = 0;
  }
  
  if (_range_fr != !digitalRead(RANGE_FR)) {
    _range_fr_count++;
    
    if (_range_fr_count > RANGE_DEB_THRESH) {
      _range_fr = !digitalRead(RANGE_FR);
    }
  } else {
    _range_fr_count = 0;
  }
  
  if (_range_bl != !digitalRead(RANGE_BL)) {
    _range_bl_count++;
    
    if (_range_bl_count > RANGE_DEB_THRESH) {
      _range_bl = !digitalRead(RANGE_BL);
    }
  } else {
    _range_bl_count = 0;
  }
  
  if (_range_br != !digitalRead(RANGE_BR)) {
    _range_br_count++;
    
    if (_range_br_count > RANGE_DEB_THRESH) {
      _range_br = !digitalRead(RANGE_BR);
    }
  } else {
    _range_br_count = 0;
  }

//  if (getDebug()) {
    uint8 msg[] = {0x16, 0x01, _range_fl<<7 | 0x00};
    serial_tx(msg,3);
    msg[2] = _range_bl << 7 | 0x01;  
    serial_tx(msg,3);
    msg[2] = _range_br << 7 | 0x02;  
    serial_tx(msg,3);
    msg[2] = _range_fr << 7 | 0x03;  
    serial_tx(msg,3); 
  
//    Serial1.print("FL: ");
//    Serial1.print(_range_fl);
//    Serial1.print(" FR: ");
//    Serial1.print(_range_fr);    
//    Serial1.print(" BL: ");
//    Serial1.print(_range_bl);    
//    Serial1.print(" BR: ");    
//    Serial1.println(_range_br);    
//  }
}

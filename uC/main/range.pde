#define RANGE_1 35
#define RANGE_2 36
#define RANGE_3 37
#define RANGE_4 24
#define RANGE_5 25
#define RANGE_6 26

#define RANGE_DEB_THRESH 10

uint8 _range_1 = 0;
uint8 _range_2 = 0;
uint8 _range_3 = 0;
uint8 _range_4 = 0;
uint8 _range_5 = 0;
uint8 _range_6 = 0;

void range_init() {
  pinMode(RANGE_1, INPUT);
  pinMode(RANGE_2, INPUT);
  pinMode(RANGE_3, INPUT);
  pinMode(RANGE_4, INPUT);
  pinMode(RANGE_5, INPUT);
  pinMode(RANGE_6, INPUT);  
}

uint8 _range_1_count = 0;
uint8 _range_2_count = 0;
uint8 _range_3_count = 0;
uint8 _range_4_count = 0;
uint8 _range_5_count = 0;
uint8 _range_6_count = 0;

void range_periodic() {
  
  if (_range_1 != !digitalRead(RANGE_1)) {
    _range_1_count++;
    
    if (_range_1_count > RANGE_DEB_THRESH) {
      _range_1 = !digitalRead(RANGE_1);
    }
  } else {
    _range_1_count = 0;
  }

  if (_range_2 != !digitalRead(RANGE_2)) {
    _range_2_count++;
    
    if (_range_2_count > RANGE_DEB_THRESH) {
      _range_2 = !digitalRead(RANGE_2);
    }
  } else {
    _range_2_count = 0;
  }

  if (_range_3 != !digitalRead(RANGE_3)) {
    _range_3_count++;
    
    if (_range_3_count > RANGE_DEB_THRESH) {
      _range_3 = !digitalRead(RANGE_3);
    }
  } else {
    _range_3_count = 0;
  }

  if (_range_4 != !digitalRead(RANGE_4)) {
    _range_4_count++;
    
    if (_range_4_count > RANGE_DEB_THRESH) {
      _range_4 = !digitalRead(RANGE_4);
    }
  } else {
    _range_4_count = 0;
  }

  if (_range_5 != !digitalRead(RANGE_5)) {
    _range_5_count++;
    
    if (_range_5_count > RANGE_DEB_THRESH) {
      _range_5 = !digitalRead(RANGE_5);
    }
  } else {
    _range_5_count = 0;
  }

  if (_range_6 != !digitalRead(RANGE_6)) {
    _range_6_count++;
    
    if (_range_6_count > RANGE_DEB_THRESH) {
      _range_6 = !digitalRead(RANGE_6);
    }
  } else {
    _range_6_count = 0;
  }


  if (getDebug()) {
//    SerialUSB.print("SRIR: ");
//    SerialUSB.println(_range_br);
    
    
    
    uint8 msg[] = {0x16, 0x01, 0x00};

    msg[2] = _range_1 << 7 | 0x00;
    serial_tx(msg,3);

    msg[2] = _range_2 << 7 | 0x01;
    serial_tx(msg,3);

    msg[2] = _range_3 << 7 | 0x02;
    serial_tx(msg,3);

    msg[2] = _range_4 << 7 | 0x03;
    serial_tx(msg,3);

    msg[2] = _range_5 << 7 | 0x04;
    serial_tx(msg,3);

    msg[2] = _range_6 << 7 | 0x05;
    serial_tx(msg,3);
 
  }
}

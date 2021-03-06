#define LRIR_1 15
#define LRIR_2 16
#define LRIR_3 17
#define LRIR_4 18
#define LRIR_5 19
#define LRIR_6 20

#define LRIR_INTTABLE_NUMENTRIES 20

uint32 _lrir_table[][2] = {{0,  4095},
                           {15, 3500},
                           {20, 3300},
                           {25, 2950}, 
                           {30, 2550},
                           {35, 2200}, 
                           {40, 1920},
                           {45, 1700},
                           {50, 1550},
                           {55, 1380}, 
                           {60, 1260},
                           {65, 1160},
                           {70, 1100},
                           {75, 1000},
                           {90,  830},
                           {105, 700},
                           {120, 600},
                           {135, 500},
                           {150, 450},
                           {1000,  0}
                          };
                                
void lrir_init() {
  pinMode(LRIR_1, INPUT_ANALOG);
  pinMode(LRIR_2, INPUT_ANALOG);
  pinMode(LRIR_3, INPUT_ANALOG);
  pinMode(LRIR_4, INPUT_ANALOG);
  pinMode(LRIR_5, INPUT_ANALOG);
  pinMode(LRIR_6, INPUT_ANALOG);  
}

float _lrir_adcToDist(uint32 adc) {
  for (uint8 idx = 0; idx < LRIR_INTTABLE_NUMENTRIES; idx++) {
    //We need to find out which range we fit in to
    if (adc > _lrir_table[idx][1]) {
      float rangeX = _lrir_table[idx][0] - _lrir_table[idx-1][0]; 
      float frac = (adc - _lrir_table[idx-1][1] * 1.0) / (_lrir_table[idx][1] * 1.0 - _lrir_table[idx-1][1]);
      return rangeX * frac + _lrir_table[idx-1][0];
    }
  }
  
}

float _lrir_reading1 = 0;
float _lrir_reading2 = 0;
float _lrir_reading3 = 0;
float _lrir_reading4 = 0;
float _lrir_reading5 = 0;
float _lrir_reading6 = 0;

void lrir_periodic() {
  _lrir_reading1 = .75 * _lrir_reading1 +  .25 * analogRead(LRIR_1);
  _lrir_reading2 = .75 * _lrir_reading2 +  .25 * analogRead(LRIR_2);
  _lrir_reading3 = .75 * _lrir_reading3 +  .25 * analogRead(LRIR_3);
  _lrir_reading4 = .75 * _lrir_reading4 +  .25 * analogRead(LRIR_4);
  _lrir_reading5 = .75 * _lrir_reading5 +  .25 * analogRead(LRIR_5);
  _lrir_reading6 = .75 * _lrir_reading6 +  .25 * analogRead(LRIR_6);  
  if (getDebug()) {

//    SerialUSB.print(_lrir_reading1);
//    SerialUSB.print(" V: ");
//    SerialUSB.print(_lrir_reading1 / 4095 * 3.3);
//    SerialUSB.print(" Dist: ");
//    
//    SerialUSB.print("LRIR1: ");
//    SerialUSB.println(_lrir_adcToDist(_lrir_reading1));
//    SerialUSB.print("LRIR2: ");
//    SerialUSB.println(_lrir_adcToDist(_lrir_reading2));
//    SerialUSB.print("LRIR3: ");
//    SerialUSB.println(_lrir_adcToDist(_lrir_reading3));
//    SerialUSB.print("LRIR4: ");
//    SerialUSB.println(_lrir_adcToDist(_lrir_reading4));
//    SerialUSB.print("LRIR5: ");
//    SerialUSB.println(_lrir_adcToDist(_lrir_reading5));
//    SerialUSB.print("LRIR6: ");
//    SerialUSB.println(_lrir_adcToDist(_lrir_reading6));


    uint8 buf[5] = {0x0b, 0x03, 0x00, 0x00, 0x00};
    uint32 dist = _lrir_adcToDist(_lrir_reading1);

    buf[2] = 0;
    buf[3] = dist & 0xFF;
    buf[4] = ((dist) >> 8) & 0xFF;
    serial_tx(buf, 5);
    
    dist = _lrir_adcToDist(_lrir_reading2);
    buf[2] = 1;
    buf[3] = dist & 0xFF;
    buf[4] = ((dist) >> 8) & 0xFF;
    serial_tx(buf, 5);
    
    dist = _lrir_adcToDist(_lrir_reading3);
    buf[2] = 2;
    buf[3] = dist & 0xFF;
    buf[4] = ((dist) >> 8) & 0xFF;
    serial_tx(buf, 5);
    
    dist = _lrir_adcToDist(_lrir_reading4);
    buf[2] = 3;
    buf[3] = dist & 0xFF;
    buf[4] = ((dist) >> 8) & 0xFF;
    serial_tx(buf, 5);
    
    dist = _lrir_adcToDist(_lrir_reading5);
    buf[2] = 4;
    buf[3] = dist & 0xFF;
    buf[4] = ((dist) >> 8) & 0xFF;
    serial_tx(buf, 5);
    
    dist = _lrir_adcToDist(_lrir_reading6);
    buf[2] = 5;
    buf[3] = dist & 0xFF;
    buf[4] = ((dist) >> 8) & 0xFF;
    serial_tx(buf, 5);
  }
 
}

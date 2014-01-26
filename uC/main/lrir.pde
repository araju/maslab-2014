#define LRIR_1 12

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
}

float _lrir_adcToDist(uint32 adc) {
  for (uint8 idx = 0; idx < LRIR_INTTABLE_NUMENTRIES - 1; idx++) {
    //We need to find out which range we fit in to
    if (adc > _lrir_table[idx][1]) {
      float rangeX = _lrir_table[idx][0] - _lrir_table[idx-1][0]; 
      float frac = (adc - _lrir_table[idx-1][1] * 1.0) / (_lrir_table[idx][1] * 1.0 - _lrir_table[idx-1][1]);
      return rangeX * frac + _lrir_table[idx-1][0];
    }
  }
  
}

float _lrir_reading1 = 0;

void lrir_periodic() {
  _lrir_reading1 = .95 * _lrir_reading1 +  .05 * analogRead(LRIR_1);
  if (getDebug()) {
    SerialUSB.print("LRIR: ");
    SerialUSB.print(_lrir_reading1);
    SerialUSB.print(" V: ");
    SerialUSB.print(_lrir_reading1 / 4095 * 3.3);
    SerialUSB.print(" Dist: ");
    SerialUSB.println(_lrir_adcToDist(_lrir_reading1));
    
  }
 
}

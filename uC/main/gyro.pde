HardwareSPI gyroSPI(1);

#define GYRO_CSPIN 10
#define GYRO_SENSOR_DATA_CMD 0x20000000

#define GYRO_DATA_OKAY_MASK 0x0C000000
#define GYRO_DATA_OKAY 0x04000000

#define GYRO_LSB_PER_DEG (.0125)

int32 _gyro_lastReading = 0;
float _gyro_degreesPerS = 0;
float _gyro_angle = 0;

void gyro_init() {
  gyroSPI.begin(SPI_1_125MHZ, MSBFIRST, SPI_MODE_0);
  pinMode(GYRO_CSPIN, OUTPUT);
  digitalWrite(GYRO_CSPIN, HIGH); 
}

int32 gyro_getAngularRate(){
  return _gyro_degreesPerS;
}

int32 gyro_getAngle() {
  return _gyro_angle;
}

void gyro_resetAngle() {
  _gyro_angle = 0;
}

void gyro_periodic(){
  int32 reading = 0;
  //Send the Sensor data command
  digitalWrite(GYRO_CSPIN, LOW);
  delayMicroseconds(10);
  reading |= gyroSPI.transfer(0x20) << 24;
//  SerialUSB.println(reading, HEX);
  delayMicroseconds(10);
  reading |= gyroSPI.transfer(0x00) << 16;
//  SerialUSB.println(reading, HEX);
  delayMicroseconds(10);
  reading |=  gyroSPI.transfer(0x00) << 8;
//  SerialUSB.println(reading, HEX);
  delayMicroseconds(10);
  reading |= gyroSPI.transfer(0x00);
//  SerialUSB.println(reading, HEX);
  delayMicroseconds(10);
  digitalWrite(GYRO_CSPIN, HIGH);
//  SerialUSB.println("");
  //If the reading is okay
  
  if (getDebug()) {
//    SerialUSB.print("Raw Reading: ");
//    SerialUSB.print(reading);
//    SerialUSB.print(" ");
//    SerialUSB.println(reading, HEX);    
  }
  
  if ((reading & GYRO_DATA_OKAY_MASK) == GYRO_DATA_OKAY) {
    //Use it
    reading = (int16)(reading >> 10) & 0x0000FFFF;
    //Taking care of sign extension
    if (reading & 0x000080000) {
      reading |= 0xFFFF0000;
    }
    _gyro_lastReading = reading;
    if (getDebug()) {
//      SerialUSB.print("Shifted: ");
//      SerialUSB.println(reading);
    }
  }else {
    //Otherwise use the last reading
//    SerialUSB.println("Bad Reading");
    reading = _gyro_lastReading;
  }
  
  int16 signedReading = (int16) reading;
  
  //This converts the angular rate from units in LSB to millidegrees
  //This works because the gain from LSB to milliDegrees is 12.5 
  //and the refresh rate is 50 hz. 12.5/50 = 1/4.  So converting to 
  //millidegrees works out to be a left shift of 2.
  _gyro_degreesPerS = -1 * signedReading * GYRO_LSB_PER_DEG;
  if (abs(_gyro_degreesPerS) > 1) {
    _gyro_angle += _gyro_degreesPerS * DT;
    if (_gyro_angle > 360) {
      _gyro_angle -= 360;
    }else if (_gyro_angle < 0) {
      _gyro_angle += 360;
    }
  }
  if (getDebug()) {
//    SerialUSB.print("Rate: ");
//    SerialUSB.print(_gyro_degreesPerS);    
//    SerialUSB.print(" Angle: ");    
//    SerialUSB.println(_gyro_angle);
  }

//  if (getDebug()) {
//    SerialUSB.println(_gyro_angle);
//  }

}

#include <HardWire.h>
#include <Wire.h>
#include <WireBase.h>

#define COLOR_SCK 29
#define COLOR_SDA 30

#define COLOR_ADDR 0x29
#define COLOR_COMMAND 0x00
#define COLOR_COMMAND_CMD 0x80
#define COLOR_COMMAND_AUTOINC 0x20

#define COLOR_ENABLE 0x00
#define COLOR_ENABLE_AIEN 0x10
#define COLOR_ENABLE_AEN 0x02
#define COLOR_ENABLE_PON 0x01

#define COLOR_ATIME 0x01
#define COLOR_ATIME_DEFAULT 0xFC

#define COLOR_CTRL 0x0F
#define COLOR_CTRL_AGAIN_X1 0x00
#define COLOR_CTRL_AGAIN_X4 0x01
#define COLOR_CTRL_AGAIN_X16 0x02
#define COLOR_CTRL_AGAIN_X64 0x03

#define COLOR_ID 0x12
#define COLOR_ID_TCS34725 0x44

#define COLOR_STATUS 0x13
#define COLOR_STATUS_VALID 0x01
#define COLOR_CLEAR_LOW 0x14

#define COLOR_RED_THRESHOLD 0x400
#define COLOR_GREEN_THRESHOLD 0x380
#define COLOR_BLUE_THRESHOLD 0x800

HardWire colorI2C(2, I2C_FAST_MODE);

void color_init() {  
//  SerialUSB.println("Color Init");
  
  //Set the integration time
  colorI2C.beginTransmission(COLOR_ADDR);
  colorI2C.send(COLOR_COMMAND_CMD | COLOR_ATIME);
  colorI2C.send(COLOR_ATIME_DEFAULT);
  colorI2C.endTransmission();
  
//  SerialUSB.println("Integration Time Set");
  //Set Gains
  colorI2C.beginTransmission(COLOR_ADDR);
  colorI2C.send(COLOR_COMMAND_CMD | COLOR_CTRL);
  colorI2C.send(COLOR_CTRL_AGAIN_X64);
  colorI2C.endTransmission();
 
  //Enable Power
//  SerialUSB.println("Gains Set");
  colorI2C.beginTransmission(COLOR_ADDR);
  colorI2C.send(COLOR_COMMAND_CMD | COLOR_ENABLE);
  colorI2C.send(COLOR_ENABLE_PON);
  colorI2C.endTransmission();

  
  delay(10);
//  SerialUSB.println("Power Enabled");  
  //Enable the ADC
  colorI2C.beginTransmission(COLOR_ADDR);
  colorI2C.send(COLOR_COMMAND_CMD | COLOR_ENABLE);
  colorI2C.send(COLOR_ENABLE_PON | COLOR_ENABLE_AEN);
  colorI2C.endTransmission();
  delay(10);
  
//  SerialUSB.println("Color End");
}

uint32 _color_clear = 0;
uint32 _color_red = 0;
uint32 _color_green = 0;
uint32 _color_blue = 0;

uint8 _color_redPresent = 0;
uint8 _color_greenPresent = 0;
uint8 _color_bluePresent = 0;

uint8 color_isRedBallPresent() {
  return _color_redPresent;
}

uint8 color_isGreenBallPresent() {
  return _color_greenPresent;
}

uint8 color_isBluePresent() {
  return _color_bluePresent;
}
void color_periodic() {
    //Read Colors
//    SerialUSB.println("Color Periodic Start");
    colorI2C.beginTransmission(COLOR_ADDR);
    colorI2C.send(COLOR_COMMAND_CMD | COLOR_COMMAND_AUTOINC | COLOR_STATUS);
    colorI2C.endTransmission();
    
//    delay(5);
    uint8 bytesRx = colorI2C.requestFrom(COLOR_ADDR, 9);
    (void) bytesRx;
    uint16 bytes[4];
//    SerialUSB.println("Color Periodic Read Done");
    if (colorI2C.receive() & COLOR_STATUS_VALID){
//      SerialUSB.println("Color Periodic Read Valid");      
      
      bytes[0] = colorI2C.receive() | colorI2C.receive() << 8;
      bytes[1] = colorI2C.receive() | colorI2C.receive() << 8;
      bytes[2] = colorI2C.receive() | colorI2C.receive() << 8;
      bytes[3] = colorI2C.receive() | colorI2C.receive() << 8;
      
      _color_clear = bytes[0];
      _color_red = bytes[1];
      _color_green = bytes[2];
      _color_blue = bytes[3];
      
      (void) _color_clear;
      
      if (_color_red > COLOR_RED_THRESHOLD && _color_red > _color_green && _color_red > _color_blue){
        //Red Ball Detected
//        SerialUSB.println("Color Red");
        _color_redPresent = 1;
      } else {
        _color_redPresent = 0;        
      }
      
      if (_color_blue > COLOR_BLUE_THRESHOLD && _color_blue > _color_green && _color_blue > _color_red) {
        _color_bluePresent = 1;
      }else {
        _color_bluePresent = 0;
      }
      
      if (_color_green > COLOR_GREEN_THRESHOLD && _color_green > _color_red && _color_green > _color_blue){
        //Green Ball Detected
//        SerialUSB.println("Color Green");        
        _color_greenPresent = 1;
      } else {
        _color_greenPresent = 0;
      }
    } else {
      bytes[0] = colorI2C.receive() | colorI2C.receive() << 8;
      bytes[1] = colorI2C.receive() | colorI2C.receive() << 8;
      bytes[2] = colorI2C.receive() | colorI2C.receive() << 8;
      bytes[3] = colorI2C.receive() | colorI2C.receive() << 8;
    }
    
//      delay(5);
    
    if (getDebug()) {
//      SerialUSB.print("R: ");
//      SerialUSB.print(_color_red);
//      SerialUSB.print(" G: ");
//      SerialUSB.print(_color_green);
//      SerialUSB.print(" B: ");
//      SerialUSB.println(_color_blue);
//      
//      if (_color_greenPresent) {
//        SerialUSB.println("Green Ball Present");
//      }
//      
//      if (_color_redPresent) {
//        SerialUSB.println("Red Ball Present");
//      }
    }
}


#include "cmd.h"
#include <stdio.h>
#include "iwdg.h"

//#define FET_PIN 24
typedef enum {
  NOT_YET_RUN,
  RUN,
  ALREADY_RAN
} 
execute_t;

void setup() {
//  Serial1.begin(230400);
  delay(1000);
  gyro_init();
  motor_init();
  sc_init();
  lrir_init();
  range_init();
//  SerialUSB.println("INIT");
//  pinMode(BOARD_LED_PIN, OUTPUT); // This pin is used for SPI, so it can't be used
//  pinMode(FET_PIN, OUTPUT);
//  digitalWrite(FET_PIN, LOW);
//  delay(1000);
//  digitalWrite(FET_PIN, HIGH);
//  SerialUSB.println("FET ON");
//  color_init(); 
  servo_init();
//  iwdg_init(IWDG_PRE_32, 500);
//  SerialUSB.println("INIT DONE");
//  pinMode(14, OUTPUT);

}



execute_t execute = NOT_YET_RUN;
uint32 clear = 0;

uint8 debug = 0;
uint8 getDebug(){
  return debug;
}

uint32 loopCounter = 0;

void loop() {
  //This is used to make sure that we only run the body of our program once per time period
//  digitalWrite(BOARD_LED_PIN, HIGH);
  uint32 currTime = millis() % LOOP_TIME;
  if (currTime == 0 && execute == NOT_YET_RUN) {
    execute = RUN;
  }
  else if (currTime != 0) {
    execute = NOT_YET_RUN;
  }

  if (millis() % 100 == 0){
      debug = 1;
  }else {
      debug = 0;
  }

  if (execute == RUN){
    digitalWrite(14, HIGH);
    if (getDebug) {
        toggleLED();
    }
     
//    if (getDebug()) {
  //    SerialUSB.print("Debug Start");
//      SerialUSB.println(millis());
//    }
//      toggleLED();
      //Here is where we list our tasks
      //Read Serial Stream and execute commands
      serial_periodic();
      //Read Gyro
      gyro_periodic(); 
  
      sc_periodic();
//     
      lrir_periodic();
  
      servo_periodic();
      range_periodic();
  //
  //    //Read Color Sensor
//      color_periodic();
      
//      iwdg_feed();
//    digitalWrite(BOARD_LED_PIN, LOW);
    if (getDebug()) {
      
//  //    SerialUSB.println("Debug End");
    }
    digitalWrite(14, LOW);
    execute = ALREADY_RAN;
  }
//  delay(100);
}







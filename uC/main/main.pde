
#include "cmd.h"

typedef enum {
  NOT_YET_RUN,
  RUN,
  ALREADY_RAN
} 
execute_t;

void setup() {
  gyro_init();
  motor_init();
//  color_init();
  sonar_init();
  //  pinMode(BOARD_LED_PIN, OUTPUT); // This pin is used for SPI, so it can't be used
  pinMode(BOARD_BUTTON_PIN, INPUT);

  delay(5000);
}



execute_t execute = NOT_YET_RUN;
uint32 clear = 0;

uint8 debug = 0;
uint8 getDebug(){
  return debug;
}

void loop() {

  //This is used to make sure that we only run the body of our program once per time period
  uint32 currTime = millis() % LOOP_TIME;
  if (currTime == 0 && execute == NOT_YET_RUN) {
    execute = RUN;
  }
  else if (currTime != 0) {
    execute = NOT_YET_RUN;
  }

  if (execute == RUN){
    
    if (millis() % 100 == 0){
      debug = 1;      
    }else {
      debug = 0;
    }
    
    //Here is where we list our tasks
    //Read Serial Stream and execute commands
    serial_periodic();
    //Read Gyro
    gyro_periodic();

    sc_periodic();

    driveSquare();
    
    sonar_periodic();

    //Read Color Sensor
//    color_periodic();
    execute = ALREADY_RAN;
  }

}







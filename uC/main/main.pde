


#include "cmd.h"

//We will run at a base loop rate of 1000/20 = 50 Hz
#define LOOP_TIME 20

typedef enum {
  NOT_YET_RUN,
  RUN,
  ALREADY_RAN
} 
execute_t;

void setup() {
  gyro_init();
  motor_init();
  color_init();
  //  pinMode(BOARD_LED_PIN, OUTPUT); // This pin is used for SPI, so it can't be used
  pinMode(BOARD_BUTTON_PIN, INPUT);
  pinMode(15, OUTPUT);
}



execute_t execute = NOT_YET_RUN;
uint32 clear = 0;

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
    
    if(millis() % 100){
//       driveSquare(); 
    }
    
    //    if (isButtonPressed()){
    //      SerialUSB.println(_gyro_milliDegrees);
    //    }
    //Here is where we list our tasks
    //Read Serial Stream and execute commands
    serial_periodic();
    //Read Gyro
//    gyro_periodic();
    //Set Left Motor
//    motor_periodic();
    //Set Right Motor

    //Send Left Motor Current

    //Send Right Motor Current

    //Set Cork Screw Drive

    //Send Cork Screw Drive Feedback

    //Control

    //Read Color Sensor
    color_periodic();
    //Set Green Gate

    //Set Red Gate

    //Set Ball Feeder


    //Update Heading and Postion Estimates

    //Speed and Heading Loop
    execute = ALREADY_RAN;
  }

}







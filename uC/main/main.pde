
#include "cmd.h"


//We will run at a base loop rate of 1000/20 = 50 Hz


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
  //  pinMode(BOARD_LED_PIN, OUTPUT); // This pin is used for SPI, so it can't be used
  pinMode(BOARD_BUTTON_PIN, INPUT);

  delay(3000);
  control_setX(100);
  control_setY(0);
  control_setTheta(-1);
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
    
    if(millis() % 200 == 0){
      SerialUSB.print("X: ");
      SerialUSB.print(state_getX());
      SerialUSB.print(" Y: ");
      SerialUSB.print(state_getY());
      SerialUSB.print(" Theta: ");
      SerialUSB.print(state_getTheta());
      SerialUSB.print(" Left: ");
      SerialUSB.print(motor_getLeftThetaDot());
      SerialUSB.print(" Right: ");
      SerialUSB.println(motor_getRightThetaDot());      
    }
    
    //Here is where we list our tasks
    //Read Serial Stream and execute commands
    serial_periodic();
    //Read Gyro
    gyro_periodic();
    //Set Left Motor
    motor_periodic();
    //Set Right Motor

    //Send Left Motor Current

    //Send Right Motor Current

    //Set Cork Screw Drive

    //Send Cork Screw Drive Feedback

    //Control

    //Read Color Sensor
//    color_periodic();
    //Set Green Gate

    //Set Red Gate

    //Set Ball Feeder

    //Update Heading and Postion Estimates
    stateEstimation_periodic();
    
    //Speed and Heading Loop
    control_periodic();
    execute = ALREADY_RAN;
  }

}







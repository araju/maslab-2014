
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
  sonar_init();
//  color_init
  //  pinMode(BOARD_LED_PIN, OUTPUT); // This pin is used for SPI, so it can't be used
  pinMode(15, OUTPUT);
  pinMode(16, OUTPUT);
  pinMode(BOARD_BUTTON_PIN, INPUT);
  delay(5000);
}


uint8 startDrive = 0;

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
  uint8 execute_slow = 0;
  if (execute == RUN){
    if (millis() % 10 == 0){
      execute_slow = 1;
    }else {
      execute_slow = 0;
    }
    
  if (millis() % 10 == 0){
    debug = 1;
  }else {
    debug = 0;
  }
    
    digitalWrite(15, HIGH);
    //Read Gyro
    gyro_periodic();
    
    //Motor Speed Control
    motor_periodic(startDrive);
    
    //Update Heading and Postion Estimates
    stateEstimation_periodic();
    
    if (execute_slow) {
      digitalWrite(16, HIGH);
      //Read Serial Stream and execute commands
      serial_periodic();
      
//      sonar_periodic();
      
      //Read Color Sensor
//      color_periodic();
      
      //Speed and Heading Loop
      if (startDrive){
        control_periodic();         
      }

      
      //Path Planner
      if (startDrive) {
        driveSquare();        
      }

      digitalWrite(16, LOW);
    }
    
    

    execute = ALREADY_RAN;
    digitalWrite(15, LOW);
  }

}







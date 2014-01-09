#include "cmd.h"
#define MOT_A_DIR 2
#define MOT_A_PWM 1
#define MOT_A_GND 0
#define MOT_B_DIR 7
#define MOT_B_PWM 6
#define MOT_B_GND 5

#define FRAME_SIZE 4

//We will run at a base loop rate of 1000/20 = 50 Hz
#define LOOP_TIME 1000

typedef enum {
  NOT_YET_RUN,
  RUN,
  ALREADY_RAN
} 
execute_t;

void setMotors(int8 velA, int8 velB);
uint16 calcPwm(int8 inputVel);
boolean calcDir(int8 inputVel);

unsigned int charCount = 0;
char buf[FRAME_SIZE];

void setup() {
  //  pinMode(BOARD_LED_PIN, OUTPUT);
  //  pinMode(MOT_A_DIR, OUTPUT);
  //  pinMode(MOT_A_PWM, PWM);
  //  pinMode(MOT_A_GND, OUTPUT);
  //  pinMode(MOT_B_DIR, OUTPUT);
  //  pinMode(MOT_B_PWM, PWM);
  //  pinMode(MOT_B_GND, OUTPUT);
  //
  //  digitalWrite(MOT_A_GND, LOW);
  //  digitalWrite(MOT_B_GND, LOW);
  //  setMotors(0, 0);

  cmd_registerCallback((uint8)'A', &cbA);
  cmd_registerCallback((uint8)'B', &cbB);
}

void cbA(uint8 *t){
  SerialUSB.println("Callback A");
}

void cbB(uint8 *t){
  SerialUSB.println("Callback B");
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
    //Here is where we list our tasks
    //Read Serial Stream and execute commands
    validMessageTest();
    queueTest();
    serial_periodic();
    //Set Left Motor

    //Set Right Motor

    //Send Left Motor Current

    //Send Right Motor Current

    //Set Cork Screw Drive

    //Send Cork Screw Drive Feedback

    //Control

    //Read Color Sensor

    //Set Green Gate

    //Set Red Gate

    //Set Ball Feeder

    //Send Ball Feeder Current


    execute = ALREADY_RAN;
  }

}

void setMotors(int8 velA, int8 velB) {
  digitalWrite(MOT_A_DIR, calcDir(velA));
  pwmWrite(MOT_A_PWM, calcPwm(velA));
  digitalWrite(MOT_B_DIR, calcDir(velB));
  pwmWrite(MOT_B_PWM, calcPwm(velB));
}

uint16 calcPwm(int8 inputVel) {
  uint16 inputVelMag = inputVel > 0 ? inputVel : -inputVel;
  uint16 pwm = (inputVelMag == 128) ? 65535 : inputVelMag << 9;
  return pwm;
}

boolean calcDir(int8 inputVel) {
  return (inputVel > 0);
}



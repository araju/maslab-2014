#ifndef CMD_H
#define CMD_H
#include "wirish.h"

#define degToRad(x) (x * 2 * pi /360.0)
#define radToDeg(x) (x * 360 / (2 * pi))

//We will run at a base loop rate of 1000/20 = 50 Hz
#define LOOP_TIME 20
#define ONE_DT 50
#define DT 0.02
#define pi 3.14159
#define sign(x) (x < 0 ? -1:1)
typedef void (*pCmdCallback)(uint8 *);
 
#endif

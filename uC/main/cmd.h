#ifndef CMD_H
#define CMD_H
#include "wirish.h"

#define degToRad(x) (x * 2 * pi /360.0)
#define radToDeg(x) (x * 360 / (2 * pi))

//We will run at a base loop rate of 1000/2 = 500 Hz
#define LOOP_TIME 2
#define DT_FAST 0.002
#define ONE_DT_FAST 500
#define ONE_DT_SLOW 100
#define DT_SLOW 0.01
#define pi 3.14159
#define sign(x) (x < 0 ? -1:1)
typedef void (*pCmdCallback)(uint8 *);
 
#endif

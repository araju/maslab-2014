#ifndef CMD_H
#define CMD_H
#include "wirish.h"

#define degToRad(x) (x * 2 * pi /360.0)
#define radToDeg(x) (x * 360 / (2 * pi))

//We will run at a base loop rate of 1000/5 = 200 Hz
#define LOOP_TIME 10
#define ONE_DT 100
#define DT (0.010 * 1.26315789)
#define pi 3.14159
#define sign(x) (x < 0 ? -1:1)
typedef void (*pCmdCallback)(uint8 *);
 
#endif

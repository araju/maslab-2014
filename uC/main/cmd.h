#ifndef CMD_H
#define CMD_H
#include "wirish.h"

#define degToRad(x) (x * 2 * pi /360.0)
#define radToDeg(x) (x * 360 / (2 * pi))
#define LOOP_TIME 20
#define ONE_DT 50
#define DT 0.02

typedef void (*pCmdCallback)(uint8 *);
 
#endif

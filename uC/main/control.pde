

#define pi 3.14159
//#define CONTROL_SPEED 12000
//#define CONTROL_STRAIGHTSPEED  9000

#define CONTROL_DIST_KP 10
//#define CONTROL_DIST_KI 5

#define CONTROL_HEADING_KP 50
//#define CONTROL_HEADING_KI 5



float _control_setPointX;
float _control_setPointY;
float _control_setPointTheta;

void control_setX(float x) {
  _control_setPointX = x;
}

void control_setY(float y) {
  _control_setPointY = y;
}

void control_setTheta(float theta) {
  _control_setPointTheta = theta;
}

void control_periodic() {
  float currX = state_getX();
  float currY = state_getY();
  float currTheta = state_getTheta();
  
  //Calculate Errors
  float distErr = sqrt(pow(_control_setPointX - currX, 2) + pow(_control_setPointY-currY,2));
  float angleErr = radToDeg(atan2(_control_setPointY - currY, _control_setPointX-currX)) - currTheta;
  //If we are more than 3 cm away from our goal then...
  if (distErr > 3){
    //If we are more than 15 degrees off of the desired heading then...
    if (angleErr > 15 || angleErr < -15){
      //Stop moving and correct your angle
      
    }else {
      //Otherwise we'll correct for angle on the way there      
      
    }
  } else {
   //Since we are now close to our goal, we should get our orientation to the desired angle
   setMotors(0,0);
  }
  
}

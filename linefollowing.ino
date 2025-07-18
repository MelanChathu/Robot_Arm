#include "MeArm.h"
#include <Servo.h>

MeArm arm;

void setup() {
  arm.begin(11, 10, 9, 6);
  arm.openClaw();
}

void loop() {
  //Go up and left to grab something
  arm.moveToXYZ(-80,100,140); 
  arm.closeClaw();
  //Go down, forward and right to drop it
  arm.moveToXYZ(70,200,10);
  arm.openClaw();
  //Back to start position
  arm.moveToXYZ(0,100,50);
}
#include <Servo.h>

// code for the land rovers with roboclaw motor controllers

// pins to send PWM to motors

#define P_M1 3
#define P_M2 9
#define P_M3 11
#define P_M4 10

Servo M1;
Servo M2;
Servo M3;
Servo M4;

// signal for motors

int s_m1;
int s_m2;
int s_m3;
int s_m4;

//     ^       ^
// M1 /         \ M2
//
//
//   ^           ^
// M4 \         / M3
//           

// input pins for recieving controls from transmitter

#define P_CH1 4
#define P_CH2 5
#define P_CH3 6
#define P_CH4 7

int ch1;
int ch2;
int ch3;
int ch4;
int ch5;
int ch6;

int surge = 0;
int  sway = 0;
int  yaw = 0;

bool inv_surge = true;
bool inv_sway = false;
bool inv_yaw = false;

bool inv_m1 = false;
bool inv_m2 = false;
bool inv_m3 = false;
bool inv_m4 = false;

int invert(int value) 
{
  return map(value, 1000, 2000, 2000, 1000);
}

void setup() {
  Serial.begin(115200);
  
  M1.attach(P_M1);
  M2.attach(P_M2);
  M3.attach(P_M3);
  M4.attach(P_M4);

  
  pinMode(P_CH1, INPUT);
  pinMode(P_CH2, INPUT);
  pinMode(P_CH3, INPUT);
  pinMode(P_CH4, INPUT);
//  pinMode(P_CH5, INPUT);
//  pinMode(P_CH6, INPUT);
}

void loop() {
  // read controls from reciever
  
  ch1 = pulseIn(P_CH1, HIGH);
  ch2 = pulseIn(P_CH2, HIGH);
  ch3 = pulseIn(P_CH3, HIGH);
  ch4 = pulseIn(P_CH4, HIGH);

  // if it is 0 the reciever or transmitter is off and it should not move at all

  if (ch1 == 0) { ch1 = 1500; }
  if (ch2 == 0) { ch2 = 1500; }
  if (ch3 == 0) { ch3 = 1500; }
  if (ch4 == 0) { ch4 = 1500; }

  // you can change this to change which stick does what

  surge = ch4;
  sway = ch1;
  yaw = ch2;

  if (inv_surge) { surge = invert(surge); }
  if (inv_sway) { sway = invert(sway); }
  if (inv_yaw) { yaw = invert(yaw); }

  // mixing the controls

  s_m1 = surge + sway + yaw - 3000;
  s_m2 = surge - sway - yaw + 3000 - 100;
  s_m3 = surge + sway - yaw;
  s_m4 = surge - sway + yaw;

  if (inv_m1) { s_m1 = invert(s_m1); }
  if (inv_m2) { s_m2 = invert(s_m2); }
  if (inv_m3) { s_m3 = invert(s_m3); }
  if (inv_m4) { s_m4 = invert(s_m4); }

// PWM should be inbetween 1000 and 2000

  s_m1 = constrain(s_m1, 1000, 2000);
  s_m2 = constrain(s_m2, 1000, 2000);
  s_m3 = constrain(s_m3, 1000, 2000);
  s_m4 = constrain(s_m4, 1000, 2000);

// this eliminates passive fluctuation in the reciever readings

  if (abs(s_m1 - 1500) <= 100) { s_m1 = 1500; }
  if (abs(s_m2 - 1500) <= 100) { s_m2 = 1500; }
  if (abs(s_m3 - 1500) <= 100) { s_m3 = 1500; }
  if (abs(s_m4 - 1500) <= 100) { s_m4 = 1500; }

//  sending the data to the motor controllers!

  M1.writeMicroseconds(s_m1);
  M2.writeMicroseconds(s_m2);
  M3.writeMicroseconds(s_m3);
  M4.writeMicroseconds(s_m4); 

//   M1.writeMicroseconds(1750);
//   delay(1000);
//   M1.writeMicroseconds(1500);
//   delay(1000);
//   M2.writeMicroseconds(1750);
//   delay(1000);
//   M2.writeMicroseconds(1500);
//   delay(1000);
//   M3.writeMicroseconds(1750);
//   delay(1000);
//   M3.writeMicroseconds(1500);
//   delay(1000);
//   M4.writeMicroseconds(1750);
//   delay(1000);
//   M4.writeMicroseconds(1500);
//   delay(1000);

//   printing to the computer for debugging

  Serial.print(" M1: ");
  Serial.print(s_m1);
  Serial.print(" M2: ");
  Serial.print(s_m2);
  Serial.print(" M3: ");
  Serial.print(s_m3);
  Serial.print(" M4: ");
  Serial.print(s_m4);
  Serial.println(" ");
}

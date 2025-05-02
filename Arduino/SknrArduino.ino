#include <Wire.h>
#include <ArduCAM.h>
#include <SPI.h>
#include "memorysaver.h"
#include <AccelStepper.h>

// MOTOR SETUP
// Define the stepper driver interface type (1 for Driver, 2 for 2-wire, 4 for 4-wire)
#define DRIVER 1
#define STEP_PIN 2
#define DIR_PIN 3
#define E_PIN 4
#define NUM_STEPS 200

#define M0 5
#define M1 6
AccelStepper stepper(DRIVER, STEP_PIN, DIR_PIN);
// standby mode for presentations
bool stdb = false;

// Define the camera module and CS pin
#define CS 10
ArduCAM myCAM(OV5642, CS);
#define laserPin 6

int pos = 0;
int s = 0;

void setup() {
  // MOTOR
  stepper.setMaxSpeed(1000);
  stepper.setSpeed(1000);
  stepper.setAcceleration(1000);
  pinMode(E_PIN, OUTPUT);
  digitalWrite(E_PIN, HIGH);

  // LASER
  pinMode(laserPin, OUTPUT);
  digitalWrite(laserPin, LOW);

  // Initialize Serial Monitor
  Wire.begin();
  // Serial.begin(921600);
  Serial.begin(2000000);
  Serial.setTimeout(50);

  // set the CS as an output:
  pinMode(CS, OUTPUT);
  digitalWrite(CS, HIGH);
  // initialize SPI:
  SPI.begin();

  myCAM.set_format(JPEG);
  myCAM.InitCAM();

  myCAM.write_reg(ARDUCHIP_TIM, VSYNC_LEVEL_MASK);   //VSYNC is active HIGH

  myCAM.write_reg(0x07, 0x80);
  delay(100);
  myCAM.write_reg(0x07, 0x00);
  delay(100);

  // Initialize the camera

  myCAM.write_reg(ARDUCHIP_MODE, 0x00);
  myCAM.OV5642_set_JPEG_size(OV5642_320x240);
  delay(1000);

  myCAM.clear_fifo_flag();
  myCAM.write_reg(ARDUCHIP_FRAMES, 0x00);

  // captureImg();
  // myCAM.CS_HIGH();  
}

void serialEvent(){
  delay(5);
  String input = Serial.readString();
  input.trim();
  String instr = input.substring(0, 3);
  // Serial.println("received " + String(instr));

  if (instr == "lon"){
    digitalWrite(laserPin, HIGH);
  }else if (instr == "lof"){
    digitalWrite(laserPin, LOW);
  }else if (instr == "cpt"){
    captureImg();
    myCAM.CS_HIGH();
  }else if (instr == "stn"){
    standby();
  }else if (instr == "mtr"){
    pos = input.substring(3, 7).toInt();
    // Serial.println("moving to " + String(pos));
    moveToPos(pos);
  }else if (instr == "tst"){
    Serial.println("This Is A Response");
  }
}

void moveToPos(int pos){
  digitalWrite(E_PIN, LOW);
  stepper.moveTo(pos);
  // while(stepper.currentPosition() != pos){
  //   stepper.runSpeedToPosition();
  // }
  stepper.runToNewPosition(pos);
  digitalWrite(E_PIN, HIGH);
  Serial.println("done");
}



void captureImg(){
  digitalWrite(laserPin, HIGH);

  myCAM.flush_fifo();
  myCAM.clear_fifo_flag();

  myCAM.start_capture();

  // Wait until capture is done
  while (!myCAM.get_bit(ARDUCHIP_TRIG, CAP_DONE_MASK));

  // Read the captured image data from FIFO
  uint32_t length = myCAM.read_fifo_length();
  // Serial.println(String(length));
  digitalWrite(laserPin, LOW);
  
  myCAM.CS_LOW();
  myCAM.set_fifo_burst();

  bool is_header = false;
  uint8_t temp =  SPI.transfer(0x00), temp_last = 0;
  length --;
  while ( length-- )
  {
    temp_last = temp;
    temp =  SPI.transfer(0x00);
    if (is_header == true)
    {
      Serial.write(temp);
    }
    else if ((temp == 0xD8) & (temp_last == 0xFF))
    {
      is_header = true;
      Serial.write(temp_last);
      Serial.write(temp);
    }
    if ( (temp == 0xD9) && (temp_last == 0xFF) ) //If find the end ,break while,
    break;
    delayMicroseconds(15);
  }  
}

void standby(){
  stepper.setSpeed(100);
  digitalWrite(E_PIN, LOW);
  digitalWrite(M0, HIGH);
  digitalWrite(M1, HIGH);
  float time = 0;
  uint32_t check = 0;

  Serial.println("st on");

  while(true){
    stepper.runSpeed();
    float val = (sin(time) + 1) * 127.5;
    // float val = millis();
    // String value = String(val);
    // Serial.println(time);
    analogWrite(laserPin, val);
    // delay(100);
    time += 0.01;
    check++;

    if (check > 4){
      String input = Serial.readString();
      input.trim();

      if (input == "stf"){
        Serial.println("st off");
        break;
      }
      check = 0;
    }
  }
  digitalWrite(E_PIN, HIGH);
  digitalWrite(M0, LOW);
  digitalWrite(M1, LOW);
}


void loop() {
}

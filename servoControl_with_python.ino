// Include the servo library
#include <Servo.h>

//declare the servo pin
int servoPin = 6;
// Create the servo object
Servo servoMotor;

char buf[8];
int pos = 0;

void setup() {
  // start a serial communication
  Serial.begin(9600);
  // connect servo object with pin
  servoMotor.attach(servoPin);

  Serial.println("Connection stalished!!");
  servoMotor.write(pos);

}

void loop() {
  while(Serial.available()){
      //pos = Serial.readBytes((char*)&pos, sizeof(pos));
      pos = Serial.read();
      Serial.print("Move to position: ");
      Serial.print(pos);
      Serial.print("\n");
      servoMotor.write(pos);
  }
}

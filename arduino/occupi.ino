/**
* OccuPi, motion sensor script
* for meeting room check
*
* This script will read the input from a
* PIR motion sensor on a digital pin
* and send it's status to the serial
* out over bluetooth
*/

int MOTION_SENSOR_PIN = 2;
int POLLING_INTERVAL = 500;

void setup(){
  // setup pins
  pinMode (MOTION_SENSOR_PIN,INPUT);
  
  // serial
  Serial.begin(9600);
}

void loop (){  
  delay(POLLING_INTERVAL); //this delay is to let the sensor settle down before taking a reading
  
  Serial.println(digitalRead(MOTION_SENSOR_PIN));
}

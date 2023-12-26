
#include "BluetoothSerial.h"

#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif
String Data;
BluetoothSerial SerialBT;

const int Mr3=26;
const int Mr4=25;
const int Mr1=12;
const int Mr2=14;


const int In1 = 13;
const int In2 = 27;
const int freq = 5000; 
const int ledChannel1 = 0; 
const int ledChannel2 = 0; 
const int resolution = 8;
const int dutyCycle=220;

//Operation for Forward
void Backward()
{
  Serial.println("Moving Backward");
  digitalWrite(Mr1,HIGH);
  digitalWrite(Mr2,LOW);
  digitalWrite(Mr3,HIGH);
  digitalWrite(Mr4,LOW);
}
//Operation for Backward
void Forward()
{
  Serial.println("Moving Forward");
  digitalWrite(Mr1,LOW);
  digitalWrite(Mr2,HIGH);
  digitalWrite(Mr3,LOW);
  digitalWrite(Mr4,HIGH);
}
//Operation for Turning Left
void Left()
{
  Serial.println("Moving Left");
  digitalWrite(Mr1,LOW);
  digitalWrite(Mr2,HIGH);
  digitalWrite(Mr3,HIGH);
  digitalWrite(Mr4,LOW);
}
//Operation for Turning Right
void Right()
{
  Serial.println("Moving Right");
  digitalWrite(Mr1,HIGH);
  digitalWrite(Mr2,LOW);
  digitalWrite(Mr3,LOW);
  digitalWrite(Mr4,HIGH);
}
//Operation for Stopping
void Stop()
{
  Serial.println("Stoping.....");
  digitalWrite(Mr1,LOW);
  digitalWrite(Mr2,LOW);
  digitalWrite(Mr3,LOW);
  digitalWrite(Mr4,LOW);
}

void setup() {
  Serial.begin(115200);
  SerialBT.begin("ESP32test"); //Bluetooth device name // <------- set this to be the same as the name you chose above!!!!!
  Serial.println("The device started, now you can pair it with bluetooth!");
  ledcSetup(ledChannel1, freq, resolution);
  ledcSetup(ledChannel2, freq, resolution);
  ledcAttachPin(In1, ledChannel1);
  ledcAttachPin(In2, ledChannel2);
  ledcWrite(ledChannel1, dutyCycle);
  ledcWrite(ledChannel2, dutyCycle);
  pinMode(Mr1,OUTPUT);
  pinMode(Mr2,OUTPUT);
  pinMode(Mr3,OUTPUT);
  pinMode(Mr4,OUTPUT);
}

void loop() {
  if (SerialBT.available()) 
  {
    Data=SerialBT.read();
    Serial.println(Data);
    if(Data=="49")
    {
      Forward();
    }
    if(Data=="48")
    {
      Stop();
    }
    if(Data=="50")
    {
      Backward();
    }
    if(Data=="51")
    {
      Left();
    }
    if(Data=="52")
    {
      Right();
    }
  }
  delay(20);
}

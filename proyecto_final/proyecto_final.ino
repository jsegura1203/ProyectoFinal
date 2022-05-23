#include <Servo.h>
#include <SoftwareSerial.h>
#include "DHT.h"
#define DHTTYPE DHT11

Servo servomotor;
const int DHTPin = 7;
int cont = 0;
int vpulsador;
String valores="";
String cadena = "";
int v[2] = {0, 0};
float h, t;

DHT dht(DHTPin, DHTTYPE);
SoftwareSerial BT(11, 10);

void setup() {
  //pulsadoR
  pinMode(6, INPUT_PULLUP);

  //DHT11
  dht.begin();

  //servomotor
  servomotor.attach(9);
  servomotor.write(90);

  //inicio de la comunicación
  Serial.begin(9600);
  Serial.setTimeout(9600);
  BT.begin(9600);
}

void loop() {

  v[0] = analogRead(A0);
  v[1] = analogRead(A1);

  v[0] = v[0] / 342 + 1;
  v[1] = v[0] / 342 + 1;

  vpulsador = digitalRead(6);

  h = dht.readHumidity() / 20 + 1; 
  t = dht.readTemperature() / 12 + 1; 
  
  valores = "I" + String(int(t)) + ";" + String(int(h)) + ";" + 
             String(v[0]) + ";" + String(v[1]) + ";" + String(!vpulsador) + "T";
             
  Serial.println(valores);
  
  if (Serial.available() > 0) 
  {
    BT.write(Serial.read());
  }
  
  if (BT.available())   
  {
    cadena = BT.read(); 
    if (cadena == "49") 
    {
      servomotor.write(180);
      delay(3000);
      servomotor.write(0);
      delay(3000);
      servomotor.write(90);
    }
    else
    {
      if (cadena == "50") 
      {
        servomotor.write(180);
        delay(1500);
        servomotor.write(0);
        delay(1500);
        servomotor.write(90);
      }
    }
  }
  delay(1000);
}

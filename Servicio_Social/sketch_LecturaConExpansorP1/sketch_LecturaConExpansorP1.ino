int contador = 0;

#include "Adafruit_PM25AQI.h"

// If your PM2.5 is UART only, for UNO and others (without hardware serial) 
// we must use software serial...
// pin #2 is IN from sensor (TX pin on sensor), leave pin #3 disconnected
// comment these two lines if using hardware serial
//#include <SoftwareSerial.h>
//SoftwareSerial pmSerial(2, 3);

#include "Wire.h"

#define TCAADDR 0x70

Adafruit_PM25AQI aqi = Adafruit_PM25AQI();

void tcaselect(uint8_t i) {
  if (i > 7) return;
 
  Wire.beginTransmission(TCAADDR);
  Wire.write(1 << i);
  Wire.endTransmission();  
}

void setup()
{
    Serial.begin(115200);
    while (!Serial);
    delay(1000);

    Wire.begin();
    
    //Serial.println("\nTCAScanner ready!");
    
    /*for (uint8_t t=0; t<8; t++) {
      tcaselect(t);
      Serial.print("TCA Port #"); Serial.println(t);

      for (uint8_t addr = 0; addr<=127; addr++) {
        if (addr == TCAADDR) continue;

        Wire.beginTransmission(addr);
        if (!Wire.endTransmission()) {
          Serial.print("Found I2C 0x");  Serial.println(addr,HEX);
          if (! aqi.begin_I2C()) {
            Serial.println("Could not find PM 2.5 sensor");
            while (1) delay(10);
          }
          Serial.println("PM25 found!");
          PM25_AQI_Data data;

  if (! aqi.read(&data)) {
    Serial.println("Could not read from AQI");
    delay(500);  // try again in a bit
    return;
  }
  

  
  Serial.println(data.pm25_standard); //Imprimir concentración 
  
  delay(1000);
        }
      }
    }*/
    //Serial.println("\ndone");
}

int arreglo8s[8] = {0,0,0,0,0,0,0,0};

void loop() 
{
  int arreglo8s[8] = {0,0,0,0,0,0,0,0};
  for (uint8_t t=0; t<8; t++) {
      tcaselect(t);
      //Serial.print("TCA Port #"); Serial.println(t);

      for (uint8_t addr = 0; addr<=127; addr++) {
        if (addr == TCAADDR) continue;

        Wire.beginTransmission(addr);
        if (!Wire.endTransmission()) {
          //Serial.print("Found I2C 0x");  Serial.println(addr,HEX);
          if (! aqi.begin_I2C()) {
            //Serial.println("Could not find PM 2.5 sensor");
            while (1) delay(10);
          }
          //Serial.println("PM25 found!");
          PM25_AQI_Data data;

          if (! aqi.read(&data)) {
          Serial.println("Could not read from AQI");
          delay(500);  // try again in a bit
          return;
          }

          arreglo8s[t] = data.pm25_standard;

          //Serial.println(data.pm25_standard); //Imprimir concentración 
  
  //delay(1000);
        }
      }
    }
    for (int i = 0; i<8; i++){
        Serial.print(arreglo8s[i]);
        Serial.print(" ");
    }
    Serial.println();
    delay(1000);
}

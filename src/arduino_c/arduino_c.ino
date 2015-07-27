#include <dht11.h>
dht11 DHT11;
#define DHT11PIN 3  // 连接数字口2

int measurePin = 0;  // 连接模拟口0
int ledPower = 2;    // 连接数字口2

int samplingTime = 280;
int deltaTime = 40;
int sleepTime = 9680;
float voMeasured = 0;
float calcVoltage = 0;
float dustDensity = 0;

void setup(){
  Serial.begin(9600);
  pinMode(ledPower,OUTPUT);
  // give the ethernet module time to boot up:
  delay(1000);
}

void loop(){
  digitalWrite(ledPower,LOW);              //开启内部LED
  delayMicroseconds(samplingTime);       // 开启LED后的280us的等待时间
  voMeasured = analogRead(measurePin);   // 读取模拟值
  delayMicroseconds(deltaTime);           //  40us等待时间
  digitalWrite(ledPower,HIGH);             // 关闭LED
  delayMicroseconds(sleepTime);

  int chk = DHT11.read(DHT11PIN);
  if (chk == DHTLIB_OK){ 
    Serial.print(voMeasured);
    Serial.print("-");
    Serial.print(analogRead(1));
    Serial.print("-");
    Serial.print(analogRead(2));
    Serial.print("-");
    Serial.print((float)DHT11.humidity, 2);
    Serial.print("-");
    Serial.print((float)DHT11.temperature, 2);
    Serial.print("-");
    Serial.println((float(voMeasured/1024)-0.0356)*120000*0.035);
  }
  delay(3000);
  Serial.flush();
}

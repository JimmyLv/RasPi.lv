String readString; 
String data;
String flag;
void setup()
{
  Serial.begin(9600);
}
void loop()
{
    while(!Serial.available()) {}
    while (Serial.available()) {
        if (Serial.available() >0) {
            char c = Serial.read();
            readString += c;
        }
    }

    if (readString.length() >0) {
        flag = "True";
        data = flag+"-"+readString+"-"+analogRead(0);
        Serial.println(data);
        readString="";
        delay(200);
    }
    Serial.flush();
}

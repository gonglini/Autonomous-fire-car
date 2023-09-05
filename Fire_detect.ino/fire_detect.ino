const int flamePin = 9; // 불꽃감지 센서의 디지털 핀 번호

int cnt = 0;
const int Detected = 5;
const int relayPin = 2;
String receivedData = "";


void setup() {
  Serial.begin(9600); 
  pinMode(flamePin, INPUT);
  pinMode(relayPin, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    receivedData = Serial.readStringUntil('\n'); 

  int flameValue = digitalRead(flamePin); // 불꽃감지 센서에서 값을 읽음

  if (flameValue == LOW) { 
    delay(500);
    cnt += 1;
    if (cnt > 10) {
      Serial.println("fire");
      cnt = 0;
      delay(1000); // 
    }
    
    if (receivedData == "s") {
      digitalWrite(relayPin, HIGH);
    }

    if(recievedData =="fire detected"){
    digitalWrite(Detected,HIGH);
    
  }
     
      // 릴레이 해제
    }
    else if (receivedData == "d") {
      digitalWrite(relayPin, LOW);
    }
    flameValue = HIGH;
    flameDetected ==LOW;
  }
  else {
    digitalWrite(relayPin, LOW); // 불꽃이 감지되지 않은 경우 릴레이를 해제
  }

}

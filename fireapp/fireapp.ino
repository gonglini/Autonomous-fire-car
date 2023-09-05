#include <ESP8266WiFi.h>

#define GPIO0 0
#define GPIO2 2

int flame = GPIO0;
int watpumf = GPIO2;

int flame_state = 0;
int watpumf_state = 0;

#define STASSID "smart1002" // SSID 입력
#define STAPSK "64047684120" // 공유기 비번 입력

const char* ssid = STASSID;
const char* password = STAPSK;

WiFiServer server(80);

bool fireDetected = false;
bool extinguishing = false;
bool extinguished = false; // 화재 진압 완료 상태를 나타내는 변수

void setup() {
  Serial.begin(9600);

  pinMode(GPIO0, INPUT);
  pinMode(GPIO2, INPUT);

  // WiFi network 연결
  Serial.println();
  Serial.println();
  Serial.print(F("Connecting to "));
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(F("."));
  }
  
  Serial.println();
  Serial.println(F("WiFi connected"));

  // 서버시작
  server.begin();
  Serial.println(F("Server started"));

  // ESP8266에 생성된 웹의 IP주소 출력
  Serial.println(WiFi.localIP());
}

void loop() {
  // 클라이언트(앱)가 접속 하는지 체크
  int flame_state = digitalRead(flame);
  int watpumf_state = digitalRead(watpumf);
  WiFiClient client = server.available(); //클라이언트를 기다리는상태

  if (client) {
    Serial.println(F("new client"));

    client.setTimeout(5000); // default is 1000

    // request의 첫 줄을 읽어온다.
    String req = client.readStringUntil('\r');
    Serial.println(F("request: "));
    Serial.println(req);

    while (client.available()) {
      client.read();
    }

    client.print(F("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")); // 반드시 전송되어야할 HTTP 헤더

    if (fireDetected) {
      client.print(F("화재 발생!!"));
    } else if (extinguishing) {
      client.print(F("사용자 확인 대기 중"));
    } else if (extinguished) {
      client.print(F("화재 진압 완료"));
      extinguished = false; // 클라이언트에게 전송한 후 화재 감지 모드로 돌아옴
    } else {
      client.print(F("화재 감지 중"));
    }

    client.stop(); // 클라이언트와 연결을 닫음
  }
  

  if (flame_state == HIGH) {
    fireDetected = true;
    extinguishing = false;
    extinguished = false;
  } else {
    fireDetected = false; 
  }


  if (watpumf_state == HIGH) {
    extinguishing = true;
    fireDetected = false;
    extinguished = false;
  } else if (extinguishing && watpumf_state == LOW) {
    extinguished = true;
    extinguishing = false;
  }
}

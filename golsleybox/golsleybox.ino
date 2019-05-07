const byte pinsw[] = {5,0,14,13};
const byte pinled[] = {16,4,2,12};

const byte SW[] = {1,1,0,0};// 1 per buto 0 for interruptors
byte State_sw[] = {0,0,0,0};

#include <Button.h>        //https://github.com/JChristensen/Button
                           //from Arduino pin 2 to ground.
#define PULLUP true        //To keep things simple, we use the Arduino's internal pullup resistor.
#define INVERT true        //Since the pullup resistor will keep the pin high unless the
                           //switch is closed, this is negative logic, i.e. a high state
                           //means the button is NOT pressed. (Assuming a normally open switch.)
#define DEBOUNCE_MS 20     //A debounce time of 20 milliseconds usually works well for tactile button switches.
#define LED_PIN 13         //The standard Arduino "Pin 13" LED

Button myBtn1(pinsw[0], PULLUP, INVERT, DEBOUNCE_MS);    //Declare the button
Button myBtn2(pinsw[1], PULLUP, INVERT, DEBOUNCE_MS);    //Declare the button
Button myBtn3(pinsw[2], PULLUP, INVERT, DEBOUNCE_MS);    //Declare the button
Button myBtn4(pinsw[3], PULLUP, INVERT, DEBOUNCE_MS);    //Declare the button

#include <Ticker.h>  //Ticker Library
 
Ticker blinker;

#include <ESP8266WebServer.h>
#include <ArduinoJson.h>

#define HTTP_REST_PORT 80
#define WIFI_RETRY_DELAY 500
#define MAX_WIFI_INIT_RETRY 50
ESP8266WebServer http_rest_server(HTTP_REST_PORT);
const char* wifi_ssid = "Jordi Soley";
const char* wifi_passwd = "eselmillorfilldelmon";

int init_wifi() {
    int retries = 0;

    Serial.println("Connecting to WiFi AP..........");
  IPAddress ip(192,168,1,200);   
  IPAddress gateway(192,168,1,254);   
  IPAddress subnet(255,255,255,0);   
  WiFi.config(ip, gateway, subnet);
    WiFi.mode(WIFI_STA);
    WiFi.begin(wifi_ssid, wifi_passwd);
    // check the status of WiFi connection to be WL_CONNECTED
    while ((WiFi.status() != WL_CONNECTED) && (retries < MAX_WIFI_INIT_RETRY)) {
        retries++;
        delay(WIFI_RETRY_DELAY);
        Serial.print("#");
    }
    return WiFi.status(); // return the WiFi connection status
}

void config_rest_server_routing() {
    http_rest_server.on("/", HTTP_GET, []() {
        http_rest_server.send(200, "text/html",
            "Welcome to the ESP8266 REST Web Server");
    });
    http_rest_server.on("/sw", HTTP_GET, get_sw);
    http_rest_server.on("/sw", HTTP_PUT, put_sw);
}



void put_sw()
{
    StaticJsonBuffer<500> jsonBuffer;
    String post_body = http_rest_server.arg("plain");
    Serial.println(post_body);

    JsonObject& jsonBody = jsonBuffer.parseObject(http_rest_server.arg("plain"));

    Serial.print("HTTP Method: ");
    Serial.println(http_rest_server.method());
    if (!jsonBody.success()) {
        Serial.println("error in parsin json body");
        http_rest_server.send(400);
    }
    else {
      if (http_rest_server.method() == HTTP_PUT) {
        http_rest_server.sendHeader("Location","ok");
        const size_t capacity = JSON_OBJECT_SIZE(1);
        DynamicJsonBuffer jsonBuffer(capacity);
        JsonObject& root = jsonBuffer.createObject();
        byte temp = jsonBody["id"];
        if(SW[temp] == 1)
        {
          if(State_sw[temp] == 1)
          {
            State_sw[temp] = 0;
            root["state"] = "Ok";
          }
          else
          {
            root["state"] = "NotOk";
          }
        }
        else
        {
          root["state"] = "SW not correcet";
        }
        char JSONmessageBuffer[400];
        root.prettyPrintTo(JSONmessageBuffer, sizeof(JSONmessageBuffer));
        http_rest_server.send(200,"application/json",JSONmessageBuffer);
            }
            else
              http_rest_server.send(404);
      
    }
}

void get_sw()
{
  const size_t capacity = JSON_ARRAY_SIZE(sizeof(SW)) + 3*JSON_OBJECT_SIZE(3);
  DynamicJsonBuffer jsonBuffer(capacity);
  char JSONmessageBuffer[400];
  JsonArray& root = jsonBuffer.createArray();
  for(int x = 0; x<sizeof(SW);x++)
  {
    JsonObject& root_0  = root.createNestedObject();
    root_0 ["id"] = x;
    root_0 ["SW_mode"] = SW[x];
    root_0 ["SW_state"] = State_sw[x];
  }
  root.prettyPrintTo(JSONmessageBuffer, sizeof(JSONmessageBuffer));
  http_rest_server.send(200, "application/json", JSONmessageBuffer);  
}
void setup() {
  Serial.begin(115200);
  if (init_wifi() == WL_CONNECTED) {
      Serial.print("Connetted to ");
      Serial.print(wifi_ssid);
      Serial.print("--- IP: ");
      Serial.println(WiFi.localIP());
  }
  else {
      Serial.print("Error connecting to: ");
      Serial.println(wifi_ssid);
  }

  config_rest_server_routing();

  http_rest_server.begin();
  Serial.println("HTTP REST Server Started");
    
  blinker.attach(0.25, ledblink); 
  for(int x= 0;x<4;x++)
  {
    pinMode(pinled[x],OUTPUT);    
  }
}






void loop() {
  http_rest_server.handleClient();
  myBtn1.read(); 
  myBtn2.read(); 
  myBtn3.read(); 
  myBtn4.read(); 
  if(myBtn1.wasReleased())
  {   
      if(State_sw[0] == 0)
      {
        State_sw[0]=1;
      }
      else
      {
        State_sw[0]=0;
      } 
  }
  if(myBtn2.wasReleased())
  {   
      if(State_sw[1] == 0)
      {
        State_sw[1]=1;
      }
      else
      {
        State_sw[1]=0;
      } 
  }
  if(myBtn3.wasReleased())
  {   
      if(State_sw[2] == 0)
      {
        State_sw[2]=1;
      }
      else
      {
        State_sw[2]=0;
      } 
  }
  if(myBtn4.wasReleased())
  {   
      if(State_sw[3] == 0)
      {
        State_sw[3]=1;
      }
      else
      {
        State_sw[3]=0;
      } 
  }
  
}

void ledblink()
{
  static byte counter = 0;
  for(int x = 0 ;x<4;x++)
  {
    if(SW[x] == 0)
    {
      digitalWrite(pinled[x],State_sw[x]);
    }
    else
    {
      if(State_sw[x]==1)
      {
        if(counter == 0)
        {
          digitalWrite(pinled[x],LOW);
        }
        else
        {
          digitalWrite(pinled[x],HIGH);
        }
      }
      else
      {
        digitalWrite(pinled[x],LOW);
      }
    }
  }
  counter++;
  if(counter==2)
  {
    counter=0;
  }
}


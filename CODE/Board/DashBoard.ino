#include "db_disp.h"      // legacy: #include "SSD1306.h"
//#include "db_interface.h"
#include "Dash_USB_serial.h"

void setup(){
    Serial.begin(115200);
    Serial.println("Board Starting");
    Serial.println("Init");
}

void loop(){
    get_serial_data();
    
    delay(1000);
}
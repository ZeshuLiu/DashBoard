#include "db_disp.h"      // legacy: #include "SSD1306.h"
#include "time_1302.h"
#include "db_interface.h"
#include "Dash_USB_serial.h"

void setup(){
    Serial.begin(115200);
    Serial.println("Board Starting");
    Serial.println("Init");
    seg_start();
    oled_start();
    led_start();
    start_RTC();
    interface_init();
    delay(100);
    interface_start();
    mode_ctrl_start();
}

void loop(){
    //get_serial_data();
    //test_clk();
    //interface_start();
    delay(1000);
}
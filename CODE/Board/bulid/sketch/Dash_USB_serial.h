#line 1 "g:\\Data\\开发\\DashBoard\\CODE\\Board\\Dash_USB_serial.h"
#ifndef DASH_USB_SERIAL_H
#define DASH_USB_SERIAL_H

#include "db_disp.h"

#define MAX_DATA_LEN 285
#define wait_time 2000
// char Serial_Data[MAX_DATA_LEN]; 
String Serial_Data = "";         // a string to hold incoming data
boolean stringComplete = false;  // whether the string is complete

void get_serial_data();
void Serial_Disp(String P_Data);

#endif
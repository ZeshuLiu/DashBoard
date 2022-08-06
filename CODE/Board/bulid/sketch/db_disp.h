#line 1 "g:\\Data\\开发\\DashBoard\\CODE\\Board\\db_disp.h"
#ifndef DB_DISP_H
#define DB_DISP_H

// SSD1306
#include <Wire.h>               
#include "SSD1306Wire.h"
#define OLED_SDA 21
#define OLED_SCL 22
SSD1306Wire display(0x3c, OLED_SDA, OLED_SCL);   // ADDRESS, SDA, SCL
#define oled_buff_len  10
String oled_buff[10] ;
bool OLED_ON = false;
// SSD1306 end
//TM1637
#include "TM1637.h"
#define TM_CLK  4 //Set the CLK pin connection to the display
#define TM_DIO  16 //Set the DIO pin connection to the display
int numCounter = 0;
bool dian = false;
bool SEG_ON = false;
TM1637 tm1637(TM_CLK, TM_DIO); //set up the 4-Digit Display.
//TM1637 end
// RGB LED
#include "Freenove_WS2812_Lib_for_ESP32.h"
#define LEDS_COUNT  24    //彩灯数目
#define LEDS_PIN  2    //ESP32控制ws2812的引脚
#define CHANNEL   1    //控制通道，最多8路
Freenove_ESP32_WS2812 led_strip = Freenove_ESP32_WS2812(LEDS_COUNT, LEDS_PIN, CHANNEL, TYPE_GRB);//申请一个彩灯控制对象
bool LED_ON = false;
// RGB LED end

//func 


void oled_start();
void seg_start();
void led_start();
void disp_test_all();
void oled_disp(int mode, int len, bool ifclear);
void seg_disp_normal(int number,int comma);
void stp_disp_round(int color[24][3]);
#endif
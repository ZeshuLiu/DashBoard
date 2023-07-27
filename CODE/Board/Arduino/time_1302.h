#ifndef TIME_1302_H
#define TIME_1302_H

#include <ThreeWire.h>  
#include <RtcDS1302.h>
#include "db_disp.h"

ThreeWire rtcWire(5,18,17); // IO, SCLK, CE
RtcDS1302<ThreeWire> Rtc(rtcWire);

void printDateTime_Serial(const RtcDateTime& dt);
void start_RTC();
void seg_clk();
void printDataTime_Seg();
void strip_clk_one();
#endif
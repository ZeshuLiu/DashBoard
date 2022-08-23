#include "time_1302.h"

#define countof(a) (sizeof(a) / sizeof(a[0]))

void start_RTC(){
    Rtc.Begin();

    RtcDateTime compiled = RtcDateTime(__DATE__, __TIME__);
    //RtcDateTime compiled = RtcDateTime("Dec 06 2009", "12:34:56");// sample input: date = "Dec 06 2009", time = "12:34:56"
    if (!Rtc.IsDateTimeValid()) {
        // Common Causes:
        //    1) first time you ran and the device wasn't running yet
        //    2) the battery on the device is low or even missing

        Serial.println("RTC lost confidence in the DateTime!");
        Rtc.SetDateTime(compiled);
    }

    if (Rtc.GetIsWriteProtected()){
        Serial.println("RTC was write protected, enabling writing now");
        Rtc.SetIsWriteProtected(false);
    }

    if (!Rtc.GetIsRunning()){
        Serial.println("RTC was not actively running, starting now");
        Rtc.SetIsRunning(true);
    }

    //Rtc.SetDateTime(compiled);
    RtcDateTime now = Rtc.GetDateTime();

    if (now < compiled) {
        Serial.println("RTC is older than compile time!  (Updating DateTime)");
        Rtc.SetDateTime(compiled);
    }
    else if (now > compiled) 
    {
        Serial.println("RTC is newer than compile time. (this is expected)");
    }
    else if (now == compiled) 
    {
        Serial.println("RTC is the same as compile time! (not expected but all is fine)");
    }
}

void printDateTime_Serial(const RtcDateTime& dt){
    char datestring[20];

    snprintf_P(datestring, 
            countof(datestring),
            PSTR("%02u/%02u/%04u %02u:%02u:%02u"),
            dt.Month(),
            dt.Day(),
            dt.Year(),
            dt.Hour(),
            dt.Minute(),
            dt.Second() 
            );
    Serial.print(datestring);
}

void printDateTime_Seg(){
        RtcDateTime now = Rtc.GetDateTime();
        int Print_time = 0;
        Print_time += now.Hour()*100;
        Print_time += now.Minute();
        seg_disp_normal(Print_time,2);
    }


void seg_clk(){
    RtcDateTime now = Rtc.GetDateTime();

    printDateTime_Serial(now);
    printDateTime_Seg();
    Serial.println();

    if (!now.IsValid()){
        // Common Causes:
        //    1) the battery on the device is low or even missing and the power line was disconnected
        Serial.println("RTC lost confidence in the DateTime!");
    }

    delay(100); // ten seconds
}

void strip_clk_one(){
    RtcDateTime now = Rtc.GetDateTime();
    int max_bright = 30;
    if (now.Hour()<8 || now.Hour()>19){
        max_bright = 15;
    }
    
    int Hour_pos = (now.Hour()+18)%24;
    int color[24][3];
    for(int i = 0; i < 24; i++){
        color[i][0] = 0;
        color[i][1] = 0;
        color[i][2] = 0;
    }
    color[Hour_pos][0] = max_bright;
    color[Hour_pos][1] = max_bright;
    color[Hour_pos][2] = max_bright;
    int Min_pos = int(int((double(now.Minute()))/2.5)+18)%24;
    color[Min_pos][0] = 0;
    color[Min_pos][1] = 0;
    color[Min_pos][2] = max_bright;
    stp_disp_round(color);
}
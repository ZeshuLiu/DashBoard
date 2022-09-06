#include <Arduino.h>
#line 1 "d:\\Data\\开发\\DashBoard\\CODE\\Board\\DashBoard.ino"
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
    //seg_clk();
    //interface_start();
    delay(1000);
}
#line 1 "d:\\Data\\开发\\DashBoard\\CODE\\Board\\Dash_USB_serial.ino"
#include "Dash_USB_serial.h"



void get_serial_data(){
    int start_time = millis();
    int j;
    Serial_Data.reserve(300);
    Serial_Data = "";
    stringComplete = false ;
    Serial.println("Listenning");
    while (millis()-start_time < wait_time){
        delay(10);
        j = Serial.available();  // 读取串口寄存器中的信息的帧数
        while(j >0){
            //delay(10);
            char inChar = Serial.read();
            Serial_Data += inChar; 
            if (inChar == '\n') {
                stringComplete = true;
            }

            j = Serial.available();

            if(stringComplete){
                if (Serial_Data=="\n"||(Serial_Data[0]-'0'>9)){
                    break;
                }
                Serial.println(Serial_Data);
                Serial_Disp(Serial_Data);
                stringComplete = false ;
                break;
            }
        }
        
    }
}

void Serial_Disp(String P_Data){
    int Po_mode ;
    int color_buff[24][3];
    int colo;
    switch (P_Data[0]- '0'){
    case 0://测试使用
        if(P_Data[1]=='0'&&P_Data[2]=='7'){
            disp_test_all();
        }
        break;
    
    case 1://Oled
        if( (P_Data[1] == '1') &&!OLED_ON){
                oled_start();
        }

        if(P_Data[1] != '1'){//end
            //oled_end();
            break;
        }
        
        Po_mode = P_Data[2] - '0';

        if(Po_mode==0){// oled mode 0
            // ST BAR
            oled_buff[0] = "";
            for (int i = 3; i <= 8; i++){
                oled_buff[0]+=P_Data[i];
            }
            oled_buff[1] = "";
            for (int i = 9; i <= 14; i++){
                oled_buff[1]+=P_Data[i];
            }
            oled_buff[2] = "";
            for (int i = 15; i <= 20; i++){
                oled_buff[2]+=P_Data[i];
            }
            //TXT
            oled_buff[3] = "";
            for (int i = 21; i <= 30; i++){
                oled_buff[3]+=P_Data[i];
            }
            oled_buff[4] = "";
            for (int i = 31; i <= 40; i++){
                oled_buff[4]+=P_Data[i];
            }
            oled_buff[5] = "";
            for (int i = 41; i <= 50; i++){
                oled_buff[5]+=P_Data[i];
            }
            oled_disp(0,1);
        }
        else{//oled_mode Wrong
            oled_disp(Po_mode,1);
        }
        
        break; // end of case 1

    case 2://SEG
        if( (P_Data[1] == '1') &&!SEG_ON){
                seg_start();
        }
        if(P_Data[1]!='1'){
            //seg_end();
            break;
        }
        if(P_Data[2]=='0'){
            seg_disp_normal((P_Data[3]-'0')*1000+(P_Data[4]-'0')*100+(P_Data[5]-'0')*10+(P_Data[6]-'0'),(P_Data[7]-'0'));
        }
        break; // end of case 2

    case 3://Strip
        if( (P_Data[1] == '1') &&!LED_ON){
                led_start();
        }
        if(P_Data[1]!='1'){
            //seg_end();
            break;
        }
        if(P_Data[2]=='0'){
            for (int i = 0; i < 24; i++){
                for (int j = 0; j < 3; j++){
                    //high
                    if(Serial_Data[i*6+3+j*2]-'0'<=9){
                        colo = (Serial_Data[i*6+3+j*2]-'0')*16;
                    }
                    else{
                        colo = (Serial_Data[i*6+3+j*2]-'a'+10)*16;
                    }

                    //low
                    if(Serial_Data[i*6+4+j*2]-'0'<=9){
                        colo += (Serial_Data[i*6+4+j*2]-'0');
                    }
                    else{
                        colo += (Serial_Data[i*6+4+j*2]-'a'+10);
                    }
                    color_buff[i][j] = colo;
                    colo = 0;
                }
            }
            stp_disp_round(color_buff);
        }
        break; // end of case 3

    default: oled_disp(-1,0);
        break;
    }
    //
}
#line 1 "d:\\Data\\开发\\DashBoard\\CODE\\Board\\db_disp.ino"
#include "db_disp.h"


void oled_start(){//SSD1306
    Serial.println("Oled Starting");
    if(!OLED_ON){
        for (int i = 0; i < oled_buff_len; i++){
            oled_buff[i] = "";
        }
        display.init();
        display.flipScreenVertically();
        display.setFont(ArialMT_Plain_10);
        OLED_ON = true;
        Serial.println("Oled Ready");
    }
}

void seg_start(){
    Serial.println("Seg Starting");
    if(!SEG_ON){// TM1637 init
        tm1637.init();
        tm1637.point(1);//小数点开关，1为打开，0为关闭
        tm1637.set(BRIGHT_TYPICAL);//BRIGHT_TYPICAL = 2,BRIGHT_DARKEST = 0,BRIGHTEST = 7;
        SEG_ON = true;
        Serial.println("Seg Ready");
    }
}

void led_start(){
    Serial.println("Led Starting");
    if(!LED_ON){// LED
        led_strip.begin();      //初始化彩灯控制引脚
        LED_ON = true;
        Serial.println("Led Ready");
    }
}

void disp_test_all(){
    oled_start();
    seg_start();
    led_start();
    for (numCounter = 0; numCounter < 9999; numCounter++){
        seg_disp_normal(numCounter,numCounter%5);
        //Serial.println("TM Disp");
        delay(20);

        oled_buff[0] = "L-Stat";
        oled_buff[1] = String(millis());// String(millis());"Right Stat";
        oled_buff[2] = "R-Stat";
        oled_buff[3] = "Sentence 1";
        oled_buff[4] = "Sentence 2";
        oled_buff[5] = "Sentence 3";
        oled_buff[6] = "Sentence 4";
        oled_disp(0,1);
        // Serial.println("Oled Disp");

        int i = 0;
        for (int t = 0; t < LEDS_COUNT; t++) {
        i = LEDS_COUNT - t-1;
        led_strip.setLedColorData(i, led_strip.Wheel((i * 256 / LEDS_COUNT + numCounter) & 255));//设置彩灯颜色数据
        }
        led_strip.show();//显示颜色
        delay(5);
        //Serial.println("Led Disp");
  }
}

void oled_disp(int mode, bool ifclear){
    if (ifclear){
        display.clear();
    }

    int sent_line = 0;
    switch (mode){
    case 0:// stat_bar_h10(L M R) Sentence_height16_left
        // stat bar
        display.setFont(ArialMT_Plain_10);
        display.setTextAlignment(TEXT_ALIGN_LEFT);
        display.drawString(0,0,oled_buff[0].substring(0,6));
        display.setTextAlignment(TEXT_ALIGN_CENTER);
        display.drawString(64,0,oled_buff[1].substring(0,6));
        display.setTextAlignment(TEXT_ALIGN_RIGHT);
        display.drawString(128,0,oled_buff[2].substring(0,6));

        // sesntence
        display.setFont(ArialMT_Plain_16);
        display.setTextAlignment(TEXT_ALIGN_LEFT);
        for (int i = 3; i < oled_buff_len; i++){
            if(oled_buff[i]!=""){
                display.drawString(0,(11+17*sent_line),oled_buff[i].substring(0,10));
            }
            sent_line += 1;
            if ((11+17*sent_line)>64){
                break;
            }
        }
        display.display();
        break; // end case 0
    

    
    default://ERR
        display.setFont(ArialMT_Plain_24);
        display.setTextAlignment(TEXT_ALIGN_CENTER_BOTH);
        display.drawString(64,32,"Mode ERR!");
        display.display();
        break;
    }
}

void seg_disp_normal(int number,int comma){
    if(comma==1){
        dian = 1;
        tm1637.point(dian);
    }
    else{
        dian = 0;
        tm1637.point(dian);
    }
    tm1637.display(0, (number / 1000%10));
    if(comma==2){
        dian = 1;
        tm1637.point(dian);
    }
    else{
        dian = 0;
        tm1637.point(dian);
    }
    tm1637.display(1, (number / 100%10));
    if(comma==3){
        dian = 1;
        tm1637.point(dian);
    }
    else{
        dian = 0;
        tm1637.point(dian);
    }
    tm1637.display(2, (number / 10%10));
    if(comma==4){
        dian = 1;
        tm1637.point(dian);
    }
    else{
        dian = 0;
        tm1637.point(dian);
    }
    tm1637.display(3, (number % 10));
}

void stp_disp_round(int color[24][3]){
    for (int i = 0; i < 24; i++){
        led_strip.setLedColor(24-i-1, color[i][0], color[i][1],color[i][2]);
        delay(2);
    }
    led_strip.show();
}
#line 1 "d:\\Data\\开发\\DashBoard\\CODE\\Board\\db_interface.ino"
#include <Arduino.h>
#include "db_interface.h"

void interface_init(){
    pinMode(CTRL_PIN, INPUT_PULLUP);
    CTRL_STAT = !digitalRead(CTRL_PIN); // high if release!

    pinMode(BOOT_PIN, INPUT_PULLUP);
    BOOT_STAT = !digitalRead(BOOT_PIN);

    pinMode(L_ENC_A, INPUT_PULLUP);
    pinMode(L_ENC_B, INPUT_PULLUP);
    L_ENC_A_STAT = digitalRead(L_ENC_A);
    L_ENC_B_STAT = digitalRead(L_ENC_B);

    pinMode(R_ENC_A, INPUT_PULLUP);
    pinMode(R_ENC_B, INPUT_PULLUP);
    R_ENC_A_STAT = digitalRead(R_ENC_A);
    R_ENC_B_STAT = digitalRead(R_ENC_B);

}

void interface_work(void *para){
    bool mid;
    bool mid2;
    for(;;){

        // ctrl pin changed
        mid = digitalRead(CTRL_PIN);
        if( CTRL_STAT == mid){
            CTRL_STAT = !CTRL_STAT;

            // ctrl released--Pressed
            if (!CTRL_STAT){
                CTRL_STAT = 0;
                CTRL_PRESS = 0;
            }
            else{
                CTRL_PRESS = 1;
            }
        }
        // ctrl end
        // boot 
        mid = digitalRead(BOOT_PIN);
        if( BOOT_STAT == mid){
            BOOT_STAT = !BOOT_STAT;

            // BOOT released--Pressed
            if (!BOOT_STAT){
                BOOT_STAT = 0;
                BOOT_PRESS = 0;
            }
            else{
                BOOT_PRESS = 1;
            }
        }
        // boot end

        //L enc
        mid = digitalRead(L_ENC_A);
        mid2 = digitalRead(L_ENC_B);
        if( L_ENC_A_STAT != mid ){ // 转动
            L_ENC_A_STAT = !L_ENC_A_STAT;
            if( L_ENC_A_STAT == mid2){
                L_ENC_RUN += 1;
            }
            else{
                L_ENC_RUN -= 1;
            }
        }
        // l enc end
        //R enc
        mid = digitalRead(R_ENC_A);
        mid2 = digitalRead(R_ENC_B);
        if( R_ENC_A_STAT != mid ){ // 转动
            R_ENC_A_STAT = !R_ENC_A_STAT;
            if( R_ENC_A_STAT == mid2){
                R_ENC_RUN += 1;
            }
            else{
                R_ENC_RUN -= 1;
            }
        }
        //R enc end
        vTaskDelay(5);
        if(DBG_interface){
            Serial.println("Go");
            Serial.printf("ctrl:%s;boot:%s;LENC:%s;RENC:%s" ,String(CTRL_PRESS),String(BOOT_PRESS),String(L_ENC_RUN),String(R_ENC_RUN));
        }

        // mode change
        if((old_ctrl != CTRL_STAT) && CTRL_STAT == 1){
            vTaskDelay(10);
            if (CTRL_STAT = digitalRead(CTRL_PIN)){
                mode = (mode+1)%max_mode ;
                mode_change = 1;
            }
        }
        old_ctrl == CTRL_STAT;
    }// 循环
}

void interface_start(){
    Serial.println("Interface start!");
    xTaskCreatePinnedToCore(
                    interface_work,          /* 任务函数 */
                    "INTERFACE",         /* 任务名 */
                    Inter_task_stack,            /* 任务栈大小，根据需要自行设置*/
                    NULL,              /* 参数，入参为空 */
                    Inter_Task_Prior,                 /* 优先级 */
                    &Inter_TASK_Handle,  /* 任务句柄 */
                    Inter_Task_Core);
}


void mode_ctrl_work(void *para){

    while (1){
        if  (mode_change){
            mode_change = 0;
            //clear_oled
            for (int i = 0; i < 10; i++){
                oled_buff[i] = " ";
            }
            oled_disp(0,1);
            //clear_led
            int mo_color[24][3];
            for(int i = 0; i < 24; i++){
                mo_color[i][0] = 0;
                mo_color[i][1] = 0;
                mo_color[i][2] = 0;
            }
            stp_disp_round(mo_color);
            seg_disp_normal(mode,0);
            vTaskDelay(1000);
            tm1637.clearDisplay();
        }

        Serial.println(String(mode));
        // mode work
        if (mode == 0){
            strip_clk_one();
            vTaskDelay(1500);
        }
        else if(mode == 1){
            get_serial_data();
            vTaskDelay(100);
        }
        else if (mode == 2){
            seg_clk();
            Serial.println("MODE 2");
            vTaskDelay(1000);
        }
        
        vTaskDelay(10);
    }//死循环
    
}

void mode_ctrl_start(){
    Serial.println("mode_ctrl start!");
    xTaskCreatePinnedToCore(
                    mode_ctrl_work,          /* 任务函数 */
                    "INTERFACE",         /* 任务名 */
                    Mode_task_stack,            /* 任务栈大小，根据需要自行设置*/
                    NULL,              /* 参数，入参为空 */
                    Mode_Task_Prior,                 /* 优先级 */
                    &Mode_TASK_Handle,  /* 任务句柄 */
                    Mode_Task_Core);
}
#line 1 "d:\\Data\\开发\\DashBoard\\CODE\\Board\\time_1302.ino"
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

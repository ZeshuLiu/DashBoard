# 1 "g:\\Data\\开发\\DashBoard\\CODE\\Board\\DashBoard.ino"
# 2 "g:\\Data\\开发\\DashBoard\\CODE\\Board\\DashBoard.ino" 2
//#include "db_interface.h"
# 4 "g:\\Data\\开发\\DashBoard\\CODE\\Board\\DashBoard.ino" 2

void setup(){
    Serial.begin(115200);
    Serial.println("Board Starting");
    Serial.println("Init");
}

void loop(){
    get_serial_data();

    delay(100);
}
# 1 "g:\\Data\\开发\\DashBoard\\CODE\\Board\\Dash_USB_serial.ino"
# 2 "g:\\Data\\开发\\DashBoard\\CODE\\Board\\Dash_USB_serial.ino" 2



void get_serial_data(){
    int start_time = millis();
    int j;
    Serial_Data.reserve(300);
    Serial_Data = "";
    stringComplete = false ;
    Serial.println("Listenning");
    while (millis()-start_time < 50){
        delay(10);
        j = Serial.available(); // 读取串口寄存器中的信息的帧数
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
# 1 "g:\\Data\\开发\\DashBoard\\CODE\\Board\\db_disp.ino"
# 2 "g:\\Data\\开发\\DashBoard\\CODE\\Board\\db_disp.ino" 2


void oled_start(){//SSD1306
    Serial.println("Oled Starting");
    if(!OLED_ON){
        for (int i = 0; i < 10; i++){
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
        tm1637.set(2);//BRIGHT_TYPICAL = 2,BRIGHT_DARKEST = 0,BRIGHTEST = 7;
        SEG_ON = true;
        Serial.println("Seg Ready");
    }
}

void led_start(){
    Serial.println("Led Starting");
    if(!LED_ON){// LED
        led_strip.begin(); //初始化彩灯控制引脚
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
        for (int t = 0; t < 24 /*彩灯数目*/; t++) {
        i = 24 /*彩灯数目*/ - t-1;
        led_strip.setLedColorData(i, led_strip.Wheel((i * 256 / 24 /*彩灯数目*/ + numCounter) & 255));//设置彩灯颜色数据
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
        for (int i = 3; i < 10; i++){
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
        delay(1);
    }
    led_strip.show();
}
# 1 "g:\\Data\\开发\\DashBoard\\CODE\\Board\\db_interface.ino"
# 2 "g:\\Data\\开发\\DashBoard\\CODE\\Board\\db_interface.ino" 2
# 3 "g:\\Data\\开发\\DashBoard\\CODE\\Board\\db_interface.ino" 2
void interface_work(void *para){
    pinMode(23, 0x05);
    CTRL_STAT = !digitalRead(23); // high if release!

    pinMode(0, 0x05);
    BOOT_STAT = !digitalRead(0);

    pinMode(19, 0x05);
    pinMode(13, 0x05);
    L_ENC_A_STAT = digitalRead(19);
    L_ENC_B_STAT = digitalRead(13);

    pinMode(34, 0x05);
    pinMode(35, 0x05);
    R_ENC_A_STAT = digitalRead(34);
    R_ENC_B_STAT = digitalRead(35);

    while (1){

        // ctrl pin changed
        if( CTRL_STAT == digitalRead(23)){
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


    }

}

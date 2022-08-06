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
        delay(1);
    }
    led_strip.show();
}
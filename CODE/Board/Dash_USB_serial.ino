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
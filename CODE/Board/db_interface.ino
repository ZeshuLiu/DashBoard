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
#include <Arduino.h>
#include "db_interface.h"
void interface_work(void *para){
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

    while (1){

        // ctrl pin changed
        if( CTRL_STAT == digitalRead(CTRL_PIN)){
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
#line 1 "g:\\Data\\开发\\DashBoard\\CODE\\Board\\db_interface.h"
#ifndef DB_INTERFACE_H
#define DB_INTERFACE_H


#define CTRL_PIN 23
bool CTRL_STAT;
bool CTRL_PRESS;

#define BOOT_PIN 0
bool BOOT_STAT;
bool BOOT_PRESS;

#define L_ENC_A 19
#define L_ENC_B 13
bool L_ENC_A_STAT;
bool L_ENC_B_STAT;
int L_ENC_RUN; // + right || - left


#define R_ENC_A 34
#define R_ENC_B 35
bool R_ENC_A_STAT;
bool R_ENC_B_STAT;
int R_ENC_RUN;// + right || - left

int ENC_SPEED_L = 1;
int ENC_SPEED_R = 1;

void interface_work(void *para);
#endif
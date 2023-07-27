#line 1 "d:\\Data\\开发\\DashBoard\\CODE\\Board\\db_interface.h"
#ifndef DB_INTERFACE_H
#define DB_INTERFACE_H

#include "db_disp.h"
#include "time_1302.h"

bool DBG_interface = 0;

TaskHandle_t Inter_TASK_Handle;
#define Inter_task_stack 10240
#define Inter_Task_Prior 7
#define Inter_Task_Core 1

TaskHandle_t Mode_TASK_Handle;
#define Mode_task_stack 10240
#define Mode_Task_Prior 4
#define Mode_Task_Core 0

#define CTRL_PIN 23
bool CTRL_STAT; //按下为1
bool CTRL_PRESS = 0;

#define BOOT_PIN 0
bool BOOT_STAT;
bool BOOT_PRESS = 0;

#define L_ENC_A 19
#define L_ENC_B 13
bool L_ENC_A_STAT;//for roting
bool L_ENC_B_STAT;//for dirction
int L_ENC_RUN = 0; // + 逆时针 || - 顺时针


#define R_ENC_A 34
#define R_ENC_B 35
bool R_ENC_A_STAT;
bool R_ENC_B_STAT;
int R_ENC_RUN = 0;// + 逆时针 || - 顺时针

int ENC_SPEED_L = 2;
int ENC_SPEED_R = 2;

bool old_ctrl = 0;
bool old_boot = 0;
int mode = 0;
int max_mode = 3;//0-time 1-serial 2-time adj
bool mode_change = 0;

void interface_init();
void interface_work(void *para);
void interface_start();
void mode_ctrl_start();
#endif
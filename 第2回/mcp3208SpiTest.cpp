#include "mcp3208Spi.h"
#include <signal.h>
#include <math.h>

#define DATA_NUM 600				//データの計測点数
//#define n 3000					//センサ交流比
//#define R 300						//中継基板抵抗値
#define X 10.0						//センサ交流比/中継基板抵抗値
#define scale_factor 3.3/4096.0		//スケールファクター

void alarmWakeup(int sig_num);		//割り込み関数宣言

int ch0_flag = 0;					//ch0制御フラグ
int calc_flag = 0;					//計算フラグ
int i = 0;							//AD変換回数のカウント変数[メイン処理用]
int cnt = 0;						//AD変換回数のカウント変数[割り込み関数用]
float OFFSET0 = 0.0;				//ch0のオフセット値格納変数
float sum = 0.0;					//AD変換値の加算値格納変数
float cur = 0.0;					//電流値(瞬時値)格納変数
float sum_cur = 0.0;				//瞬時値2乗の加算値格納変数
float Ie = 0.0;						//電流値(実効値)格納変数
int a2dVal0[DATA_NUM];				//ch0のAD変換値格納配列
unsigned char data_s[3];			//AD変換のch制御ビット格納配列

mcp3208Spi a2d("/dev/spidev0.0", SPI_MODE_0, 2000000, 8);

using namespace std;


int main(void)		//メイン関数
{
	signal(SIGALRM, alarmWakeup); 
	ch0_flag = 1;  
	ualarm(1, 100);		//void alarmWakeup関数を開始

	while(1)			//メインループ
	{
		if(calc_flag == 1)
		{
			ualarm(0,0);				//void alarmWakeup関数を停止
			if(OFFSET0 == 0.0)			//オフセット値計算（初回のみ）
			{
				for(i=0;i<DATA_NUM;i++)
				{
					sum += (float)a2dVal0[i];
				}
				usleep(100);
				OFFSET0 = sum /(float)DATA_NUM;
				cout << "OFFSET0: " << OFFSET0 << endl;

			}
			for(i=0; i<DATA_NUM; i++)	
			{
				cur = ((float)a2dVal0[i] - OFFSET0)*(scale_factor)*X;
				sum_cur += cur*cur;
			}
			
			Ie = sqrt(sum_cur/(float)DATA_NUM);		//実効値算出

			cout << "Ie: " << Ie <<"[A]"<<endl;
			cout << "-------------------------" << endl;	

			sum = 0.0;
			cur = 0.0;
			sum_cur = 0.0;
			Ie = 0.0;
			cnt=0;
         	ch0_flag=1;
			calc_flag=0;

         	sleep(1);
			ualarm(1,100);		//void alarmWakeup関数を開始
		}
	}
	return 0;
}






void alarmWakeup(int sig_num)
{
	if(ch0_flag == 1)		//ch0のAD変換処理
	{	    
		if(cnt<DATA_NUM)
		{
			if(sig_num == SIGALRM)
			{
				data_s[0] = 0b00000110; 
				data_s[1] = 0b00000000; 
				//data_s[2] = 0b00000000; 

				a2d.spiWriteRead(data_s, sizeof(data_s) );	//SPI通信       

				a2dVal0[cnt] = 0;
				a2dVal0[cnt] = (data_s[1]<< 8) & 0b111100000000;  	//AD変換結果data_s[1]からB11-B8のみを抜き出す
				a2dVal0[cnt] |=  (data_s[2]);						//data_s[2]をdata_s[2]と結合
			}
				cnt++;
                        
				if(cnt==DATA_NUM)
				{
					ch0_flag = 0;	
					calc_flag = 1;
					cnt=0;
				}
		}
	}
}

#include<stdio.h>
#include<stdlib.h>
#include<cmath>
#include<time.h>
#include <chrono>
#include <thread>

double deg2rad(double deg)
{
    return deg * M_PI/180;
}

double* dgist_gait_gen(int &counter)
{
    //Gait Parameters
    int gait_type = 2; //0 : vertical, 1 : Sinuous, 2 : Sidewind
    double d_amp = 30;
    double d_phase = 60;
    double l_amp = 30;
    double l_phase = 60;
    int tau = 1;

    //뱀 로봇 목표 각도 배열
    // double joints_goal[14];
    double *joints_goal = (double *)malloc(14*sizeof(double));

    //1ms로 들어온다고 했을 때, 슬롯 타임 보상기
    int t_slot = 5;

    //DGIST Gait 생성은 5ms로 되어있으므로,
    if( (counter % (t_slot * tau)) == 0)
    {
        // printf("inside of func...\n");
        int k = counter / (t_slot * tau);

        double P[14] = \
        {\
        0,\
        0,\
        0,\
        0,\
        0,\
        0,\
        0,\
        0,\
        0,\
        0,\
        0,\
        0,\
        0,\
        0\
        };

        //gait에 맞는 P함수 생성
        for(int idx = 0; idx < 14; idx++)
        {
            if(gait_type == 1) // Vertical
            {
                if(idx%2 == 0)
                {
                    //Even number (ex:1,3,5th... joint from head.)
                    P[idx] = d_amp * sin((2 * M_PI / 8) * k + idx * deg2rad(d_phase));
                }
                else
                {
                    //Odd number (ex:2,4,6th... joint from head.)
                    P[idx] = l_amp * sin((M_PI / 8) * k + ((idx * 0.5) + 1) * deg2rad(l_phase));
                }
            }
            else if(gait_type == 2)
            {
                if(idx%2 == 0)
                {
                    //Even number (ex:1,3,5th... joint from head.)
                    P[idx] = d_amp * sin((2 * M_PI / 8) * k + ((idx * 0.5) + 0.5) * deg2rad(d_phase));
                }
                else
                {
                    //Odd number (ex:2,4,6th... joint from head.)
                    P[idx] = l_amp * sin((M_PI / 8) * k + (idx - 1) * deg2rad(l_phase));
                }
            }
        }

        // Motion 행렬 구성
        int M_vert[14][8] =\
        {\
        {1,0,0,0,0,0,0},\
        {0,0,0,0,0,0,0},\
        {0,1,0,0,0,0,0},\
        {0,0,0,0,0,0,0},\
        {0,0,1,0,0,0,0},\
        {0,0,0,0,0,0,0},\
        {0,0,0,1,0,0,0},\
        {0,0,0,0,0,0,0},\
        {0,0,0,0,1,0,0},\
        {0,0,0,0,0,0,0},\
        {0,0,0,0,0,1,0},\
        {0,0,0,0,0,0,0},\
        {0,0,0,0,0,0,1},\
        {0,0,0,0,0,0,0}\
        };

        int M_sin[14][14] =\
        {\
        {1,0,0,0,0,0,0,0,0,0,0,0,0,0},\
        {0,1,0,0,0,0,0,0,0,0,0,0,0,0},\
        {0,0,1,0,0,0,0,0,0,0,0,0,0,0},\
        {0,0,0,1,0,0,0,0,0,0,0,0,0,0},\
        {0,0,0,0,1,0,0,0,0,0,0,0,0,0},\
        {0,0,0,0,0,1,0,0,0,0,0,0,0,0},\
        {0,0,0,0,0,0,1,0,0,0,0,0,0,0},\
        {0,0,0,0,0,0,0,1,0,0,0,0,0,0},\
        {0,0,0,0,0,0,0,0,1,0,0,0,0,0},\
        {0,0,0,0,0,0,0,0,0,1,0,0,0,0},\
        {0,0,0,0,0,0,0,0,0,0,1,0,0,0},\
        {0,0,0,0,0,0,0,0,0,0,0,1,0,0},\
        {0,0,0,0,0,0,0,0,0,0,0,0,1,0},\
        {0,0,0,0,0,0,0,0,0,0,0,0,0,1}
        };
        int M_side[14][14] =\
        {\
        {0,1,0,0,0,0,0,0,0,0,0,0,0,0},\
        {1,0,0,0,0,0,0,0,0,0,0,0,0,0},\
        {0,0,0,1,0,0,0,0,0,0,0,0,0,0},\
        {0,0,1,0,0,0,0,0,0,0,0,0,0,0},\
        {0,0,0,0,0,1,0,0,0,0,0,0,0,0},\
        {0,0,0,0,1,0,0,0,0,0,0,0,0,0},\
        {0,0,0,0,0,0,0,1,0,0,0,0,0,0},\
        {0,0,0,0,0,0,1,0,0,0,0,0,0,0},\
        {0,0,0,0,0,0,0,0,0,1,0,0,0,0},\
        {0,0,0,0,0,0,0,0,1,0,0,0,0,0},\
        {0,0,0,0,0,0,0,0,0,0,0,1,0,0},\
        {0,0,0,0,0,0,0,0,0,0,1,0,0,0},\
        {0,0,0,0,0,0,0,0,0,0,0,0,0,1},\
        {0,0,0,0,0,0,0,0,0,0,0,0,1,0}
        };

        if(gait_type == 0)
        {

        }
        else if(gait_type == 1)
        {
            for(int idx = 0; idx < 14; idx++)
            {
                joints_goal[idx] = P[idx] * M_sin[idx][(k%14)];
            }
        }
        else if(gait_type == 2)
        {
            for(int idx = 0; idx < 14; idx++)
            {
                joints_goal[idx] = P[idx] * M_side[idx][(k%14)];
            }
        }

        // //For debugging... (P func print...)
        // printf("[");
        // for(int idx = 0; idx < sizeof(P) / sizeof(double); idx++)
        // {
        //     printf(" %f",P[idx]);
        // }
        // printf(" ]\n");

        //For debugging... (joint goals print...)
        // printf("[");
        // for(int idx = 0; idx < 14; idx++)
        // {
        //     printf(" %f",joints_goal[idx]);
        // }
        // printf(" ]\n");
    }
    else
    {
        for(int idx = 0; idx < 14; idx++)
        {
            joints_goal[idx] = 0;
        }
    }

    // printf("outside of func...\n");
    counter++;
    free(joints_goal);

    return joints_goal;
}

int main(int argc, char **argv)
{
    static int counter = 0;

    while (1)
    {
        double *angles = dgist_gait_gen(counter);

        //For debugging... (joint goals print...)
        printf("[");
        for(int idx = 0; idx < 14; idx++)
        {
            printf(" %f",angles[idx]);
        }
        printf(" ]\n");

        std::this_thread::sleep_for(std::chrono::microseconds(300000));
    }

    return 0;
}
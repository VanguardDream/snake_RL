/* © 2021 Bongsub Song <doorebong@gmail.com>
 All right reserved
 Description : BRM snake robot KIRO integrated function
*/

#include<math.h>
#include<stdio.h>
#include<stdlib.h>

void dgistmotion()
{
//DGIST Gait Decomposition 실증용 Cpp코드
	//호출 횟수 카운트를 위한 정적 변수
	static int counter = 0;
	int com_idx;

	//Gait Parameters
	int gait_type = 2; //0 : vertical, 1 : Sinuous, 2 : Sidewind
	double d_amp = 48.0;
	double d_phase = 233.0;
	double l_amp = 48.6;
	double l_phase = 39.3;
	int tau = 2;

	//뱀 로봇 목표 각도 배열
	float joints_goal[14];
	float temp_goal[14];
	//double* joints_goal = (double*)malloc(14 * sizeof(double));

	//DGIST Gait 생성은 5ms로 되어있으므로,
	if ((counter % (tau)) == 0)
	{
		// printf("inside of func...\n");
		int k = counter / tau;
		com_idx = k % 14;


		double P[14] = \
		{\
			0, \
			0, \
			0, \
			0, \
			0, \
			0, \
			0, \
			0, \
			0, \
			0, \
			0, \
			0, \
			0, \
			0\
		};

		//gait에 맞는 P함수 생성
		for (int idx = 0; idx < 14; idx++)
		{
			if (gait_type == 1) // Vertical
			{
				if (idx % 2 == 0)
				{
					//Even number (ex:1,3,5th... joint from head.)
					P[idx] = d_amp * sin((2 * M_PI / 8) * k + idx * (d_phase * M_PI / 180));
				}
				else
				{
					//Odd number (ex:2,4,6th... joint from head.)
					P[idx] = l_amp * sin((M_PI / 8) * k + ((idx * 0.5) + 1) * (l_phase * M_PI / 180));
				}
			}
			else if (gait_type == 2)
			{
				if (idx % 2 == 0)
				{
					//Even number (ex:1,3,5th... joint from head.)
					P[idx] = d_amp * sin((2 * M_PI / 8) * k + ((idx * 0.5) + 0.5) * (d_phase * M_PI / 180));
				}
				else
				{
					//Odd number (ex:2,4,6th... joint from head.)
					P[idx] = l_amp * sin((M_PI / 8) * k + (idx - 1) * (l_phase * M_PI / 180));
				}
			}
		}

		// Motion 행렬 구성
		int M_vert[14][8] = \
		{\
		{1, 0, 0, 0, 0, 0, 0}, \
		{0, 0, 0, 0, 0, 0, 0}, \
		{0, 1, 0, 0, 0, 0, 0}, \
		{0, 0, 0, 0, 0, 0, 0}, \
		{0, 0, 1, 0, 0, 0, 0}, \
		{0, 0, 0, 0, 0, 0, 0}, \
		{0, 0, 0, 1, 0, 0, 0}, \
		{0, 0, 0, 0, 0, 0, 0}, \
		{0, 0, 0, 0, 1, 0, 0}, \
		{0, 0, 0, 0, 0, 0, 0}, \
		{0, 0, 0, 0, 0, 1, 0}, \
		{0, 0, 0, 0, 0, 0, 0}, \
		{0, 0, 0, 0, 0, 0, 1}, \
		{0, 0, 0, 0, 0, 0, 0}\
		};

		int M_sin[14][14] = \
		{\
		{1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, \
		{0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, \
		{0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, \
		{0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, \
		{0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0}, \
		{0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0}, \
		{0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0}, \
		{0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0}, \
		{0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0}, \
		{0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0}, \
		{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0}, \
		{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0}, \
		{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0}, \
		{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1}
		};
		int M_side[14][14] = \
		{\
		{0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, \
		{1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, \
		{0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, \
		{0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}, \
		{0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0}, \
		{0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0}, \
		{0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0}, \
		{0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0}, \
		{0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0}, \
		{0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0}, \
		{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0}, \
		{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0}, \
		{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1}, \
		{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0}
		};

		if (gait_type == 0)
		{

		}
		else if (gait_type == 1)
		{
			for (int idx = 0; idx < 14; idx++)
			{
				joints_goal[idx] = P[idx] * M_sin[idx][(k % 14)];
			}
		}
		else if (gait_type == 2)
		{
			for (int idx = 0; idx < 14; idx++)
			{
				joints_goal[idx] = P[idx] * M_side[idx][(k % 14)];
			}
		}

		for (int idx = 0; idx < 14; idx++)
		{
			if (fabs(joints_goal[idx] - 0) > 0.2)
			{
				targetPosition[13-idx] = joints_goal[idx];
			}
		}

	}
	else
	{
		for (int idx = 0; idx < 14; idx++)
		{
			joints_goal[idx] = 0;
		}
	}

	counter++;
}
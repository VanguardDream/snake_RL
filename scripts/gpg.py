# import mujoco_py
import os
import random
import gait

# def main():
#     g = gait.gait()


# if __name__ == "__main__":
#     main()

g = gait.gait(2,tau=1)

for i in range(0,15):
    print(g.generate(i))
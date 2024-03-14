clc; clear;
%%
T = vecnorm(head_acc_log, 2, 2)

figure;
plot(T)

mean(T)
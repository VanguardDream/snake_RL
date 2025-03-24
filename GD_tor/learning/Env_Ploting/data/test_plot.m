clc; clear;
load rl_data.mat
%%
real_ftd = movmean(raw_data,10);


%%
figure;
plot(ftd_data);

figure;
plot(real_ftd);
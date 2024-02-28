clc; clear;
%%
% load Serp_Curve.mat;
load Side_Curve.mat
U_curve = U_map;

clear U_map Motion_lambda

load Serp_Mat.mat;
U_mat_serp = U_map;

clear U_map Motion_lambda

load Side_Mat.mat;
U_mat_side = U_map;

clear U_map Motion_lambda

load Slit_Mat.mat;
U_mat_slit = U_map;

clear U_map Motion_lambda
%%
hold on;
grid on;
scatter3(U_curve(:,3),U_curve(:,4),U_curve(:,5))
scatter3(U_mat_serp(:,3),U_mat_serp(:,4),U_mat_serp(:,5))
scatter3(U_mat_side(:,3),U_mat_side(:,4),U_mat_side(:,5))
scatter3(U_mat_slit(:,3),U_mat_slit(:,4),U_mat_slit(:,5))

xlabel("X-axis vel")
ylabel("Y-axis vel")
zlabel("Ang vel")
%%
% load trajectory_M_45x45x30x30x30x30x0x0_05_Bar_45x45x30x30x30x30x0x0_05.mat;
% load trajectory_M_45x45x30x30x60x30x0x0_05_Bar_45x45x30x30x60x30x0x0_05.mat;

% t = trajectory_M_45x45x30x30x30x30x0x0_05_Bar_45x45x30x30x30x30x0x0;
% t = trajectory_M_45x45x30x30x60x30x0x0_05_Bar_45x45x30x30x60x30x0x0;
k = 0:0.005:9.99999;
d_t = diff(t) / 0.005;

figure
plot(k,d_t(:,1:2));

figure
plot(k,d_t(:,3:5));

d_mvt = movmean(d_t,20);

figure
plot(k, d_mvt(:,1:2));
figure
plot(k, d_mvt(:,3:5));

mean(d_t)
mean(d_mvt)
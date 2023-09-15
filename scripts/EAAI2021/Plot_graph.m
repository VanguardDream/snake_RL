clc; clear;

load('serp_U_total.mat');

% OP 페이즈 고정 후 각도만 확인 
% Serp Op 파라미터 [39.8, 189.9, -9.1, 66.5, 160.9, 7.0, 1]

OP_dA_lA = squeeze(U(:, 20, :, 17));

surf(OP_dA_lA);
zlim([-3000, 3000]);
clim([-3000 3000])
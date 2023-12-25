clc; clear;
%%
% load grid_map_serp_b_7x7x14x7x0x0x0_129600_.mat
load grid_map_serp_b_7x11x14x7x0x0x0_129600_servo.mat

%%
serp_map = squeeze(serp_grid);

sz = size(serp_map);

[a, b] = size(sz);
if b >= 2
    n_d = 1:1:sz(end-2);
    n_l = 1:1:sz(end-1);
end
if b >= 4
    o_d = 1:1:sz(end-4);
    o_l = 1:1:sz(end-3);
end
if b >= 6
    a_d = 1:1:sz(end-6);
    a_l = 1:1:sz(end-5);
end
clear a b;

U_serp = serp_map(:,:,1);

clear dX dY;

U_serp = max(U_serp, -2000);

%% U Grid
U_serp = transpose(U_serp); %이유는 모르지만 계속 X,Y 값이 바뀌어 있음.
figure(Name='Utility grid map');
mesh(n_l, n_d, U_serp);
xlabel("Dorsal Spatial");
ylabel("Lateral Spatial");

view([0 90])

%% Argmax in matrix
[C,I] = max(U_serp(:));

[I1,I2] = ind2sub(size(U_serp),I);
U_serp(I1,I2)
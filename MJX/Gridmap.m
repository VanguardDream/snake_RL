clc; clear;
%%
load grid_map_serp_b_7x7x14x7x0x0x0_129600_.mat

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
figure(Name='Utility grid map');
surf(n_d, n_l, U_serp);
xlabel("Dorsal Spatial");
ylabel("Lateral Spatial");



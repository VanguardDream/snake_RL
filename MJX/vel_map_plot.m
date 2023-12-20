clc; clear;
%%
% load vel_map_serp_b_7x7x14x7x0x0x0_256_.mat;
% load vel_map_side_b_7x7x14x7x0x0x0_256_.mat;
% load vel_map_ones_b_7x7x14x7x0x0x0_256_.mat;

load vel_map_ones_b_7x7x7x7x0x0x0_20736_.mat;
load vel_map_serp_b_7x7x7x7x0x0x0_20736_.mat;
load vel_map_side_b_7x7x7x7x0x0x0_20736_.mat;

serp_map = squeeze(serp_map);
side_map = squeeze(side_map);
ones_map = squeeze(ones_map);

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

for dX = 1:1:n_d(end);
    for dY = 1:1:n_l(end);
        T_serp(dX,dY) = transpose(norm(squeeze(serp_map(dX,dY,1:3))));
        T_side(dX,dY) = transpose(norm(squeeze(side_map(dX,dY,1:3))));
        T_ones(dX,dY) = transpose(norm(squeeze(ones_map(dX,dY,1:3))));
    end
end

clear dX dY;

% T_serp = float(sqrt(serp_map(:,:,1)^2 + serp_map(:,:,2)^2 + serp_map(:,:,3)^2));
% T_side = sqrt(side_map(:,:,1)^2 + side_map(:,:,2)^2 + side_map(:,:,3)^2);
% T_ones = sqrt(ones_map(:,:,1)^2 + ones_map(:,:,2)^2 + ones_map(:,:,3)^2);



for dX = 1:1:sz(1);
    for dY = 1:1:sz(2);
        Q_serp(dX,dY) = quaternion(transpose(squeeze(serp_map(dX,dY,4:7))));
        Q_side(dX,dY) = quaternion(transpose(squeeze(side_map(dX,dY,4:7))));
        Q_ones(dX,dY) = quaternion(transpose(squeeze(ones_map(dX,dY,4:7))));
    end
end

clear dX dY;

for dX = 1:1:sz(1);
    for dY = 1:1:sz(2);
        R_serp(dX,dY,1:3) = rotvecd(squeeze(Q_serp(dX,dY)));
        R_side(dX,dY,1:3) = rotvecd(squeeze(Q_side(dX,dY)));
        R_ones(dX,dY,1:3) = rotvecd(squeeze(Q_ones(dX,dY)));
    end
end

clear dX dY;
%% L Velocities
figure(Name='Serp Total Velocity');
surf(n_d, n_l, T_serp(n_d,n_l));
xlabel("Dorsal Spatial");
ylabel("Lateral Spatial");

figure(Name='Side Total Velocity');
surf(n_d, n_l, T_side(n_d,n_l));
xlabel("Dorsal Spatial");
ylabel("Lateral Spatial");

figure(Name='Ones Total Velocity');
surf(n_d, n_l, T_ones(n_d,n_l));
xlabel("Dorsal Spatial");
ylabel("Lateral Spatial");
%%
figure(Name='Serp X axis Linear Velocity');
surf(n_d * (1/8 * pi), n_l * (1/8 * pi), serp_map(n_d,n_l,1));
xlabel("Dorsal Spatial");
ylabel("Lateral Spatial");

figure(Name='Side X axis Linear Velocity');
surf(n_d * (1/8 * pi), n_l * (1/8 * pi), side_map(n_d,n_l,1));
xlabel("Dorsal Spatial");
ylabel("Lateral Spatial");

figure(Name='Ones X axis Linear Velocity');
surf(n_d * (1/8 * pi), n_l * (1/8 * pi), ones_map(n_d,n_l,1));
xlabel("Dorsal Spatial");
ylabel("Lateral Spatial");

%%
figure(Name='Serp Y axis Linear Velocity');
surf(n_d * (1/8 * pi), n_l * (1/8 * pi), serp_map(n_d,n_l,2));
xlabel("Dorsal Spatial");
ylabel("Lateral Spatial");

figure(Name='Side Y axis Linear Velocity');
surf(n_d * (1/8 * pi), n_l * (1/8 * pi), side_map(n_d,n_l,2));
xlabel("Dorsal Spatial");
ylabel("Lateral Spatial");

figure(Name='Ones Y axis Linear Velocity');
surf(n_d * (1/8 * pi), n_l * (1/8 * pi), ones_map(n_d,n_l,2));
xlabel("Dorsal Spatial");
ylabel("Lateral Spatial");

%% A Velocities
figure(Name='Serp X axis Angular Velocity');
surf(n_d * (1/8 * pi), n_l * (1/8 * pi), R_serp(n_d,n_l,1));
xlabel("Dorsal Spatial");
ylabel("Lateral Spatial");

figure(Name='Side X axis Angular Velocity');
surf(n_d * (1/8 * pi), n_l * (1/8 * pi), R_side(n_d,n_l,1));
xlabel("Dorsal Spatial");
ylabel("Lateral Spatial");

figure(Name='Ones X axis Angular Velocity');
surf(n_d * (1/8 * pi), n_l * (1/8 * pi), R_ones(n_d,n_l,1));
xlabel("Dorsal Spatial");
ylabel("Lateral Spatial");

figure(Name='Serp Y axis Angular Velocity');
surf(n_d * (1/8 * pi), n_l * (1/8 * pi), R_serp(n_d,n_l,2));
xlabel("Dorsal Spatial");
ylabel("Lateral Spatial");

figure(Name='Side Y axis Angular Velocity');
surf(n_d * (1/8 * pi), n_l * (1/8 * pi), R_side(n_d,n_l,2));
xlabel("Dorsal Spatial");
ylabel("Lateral Spatial");

figure(Name='Ones Y axis Angular Velocity');
surf(n_d * (1/8 * pi), n_l * (1/8 * pi), R_ones(n_d,n_l,2));
xlabel("Dorsal Spatial");
ylabel("Lateral Spatial");

figure(Name='Serp Z axis Angular Velocity');
surf(n_d * (1/8 * pi), n_l * (1/8 * pi), R_serp(n_d,n_l,3));
xlabel("Dorsal Spatial");
ylabel("Lateral Spatial");

figure(Name='Side Z axis Angular Velocity');
surf(n_d * (1/8 * pi), n_l * (1/8 * pi), R_side(n_d,n_l,3));
xlabel("Dorsal Spatial");
ylabel("Lateral Spatial");

figure(Name='Ones Z axis Angular Velocity');
surf(n_d * (1/8 * pi), n_l * (1/8 * pi), R_ones(n_d,n_l,3));
xlabel("Dorsal Spatial");
ylabel("Lateral Spatial");


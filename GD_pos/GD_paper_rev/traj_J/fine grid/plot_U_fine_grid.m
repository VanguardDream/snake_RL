clc; clear;

%% load
% load U_traj_fine_True_0.3_45x45x158x158x115x115x0x0_05_21901_.mat
% load U_traj_fine_True_0.3_45x45x32x32x116x58x0x0_05_21901_.mat
% load U_traj_fine_True_0.3_45x45x159x159x85x85x45x0_05_21901_.mat
load U_traj_fine_True_0.3_15x15x169x169x119x119x90x0_05_21901_.mat

U_map_curve = U_map;
Rot_vec_curve = Rot_vec;
Tf_orientation_curve = Tf_orientation;

clear max min Motion_lambda param_coefficient U_map Rot_vec Tf_orientation;

% load U_traj_fine_False_0.3_serp.mat
% load U_traj_fine_False_0.5_serp.mat
% load U_traj_fine_False_0.7_serp.mat
% load U_traj_fine_False_0.9_serp.mat

% load U_traj_fine_False_0.3_slit.mat
% load U_traj_fine_False_0.5_slit.mat
% load U_traj_fine_False_0.7_slit.mat
% load U_traj_fine_False_0.9_slit.mat

% load U_traj_fine_False_0.3_side.mat
% load U_traj_fine_False_0.5_side.mat
% load U_traj_fine_False_0.7_side.mat
% load U_traj_fine_False_0.9_side.mat

% load U_traj_fine_False_0.3_roll.mat
load U_traj_fine_False_0.5_roll.mat
% load U_traj_fine_False_0.7_roll.mat
% load U_traj_fine_False_0.9_roll.mat

U_map_mat = U_map;
Rot_vec_mat = Rot_vec;
Tf_orientation_mat = Tf_orientation;

clear max min Motion_lambda param_coefficient U_map Rot_vec Tf_orientation;

U_map_curve = transpose(U_map_curve);
U_map_mat = transpose(U_map_mat);

Tf_orientation_curve = transpose(Tf_orientation_curve);
Tf_orientation_mat = transpose(Tf_orientation_mat);
%%
U_map_mat = squeeze(U_map_mat);
U_map_curve = squeeze(U_map_curve);

U_map_mat = max(U_map_mat, -1000);
U_map_curve = max(U_map_curve, -1000);
% 
% U_map_mat = min(U_map_mat, 900);
% U_map_curve = min(U_map_curve, 900);

% fixed_c_axis = [100 900];

%% 끝점 방위 값 연동
U_map_curve = U_map_curve - 500 * abs(Tf_orientation_curve);
U_map_mat = U_map_mat - 500 * abs(Tf_orientation_mat);

%%
figure; hAxes = gca;
contourf(U_map_curve);

pbaspect([1 1 0.8]);

colormap jet;
colorbar;

yticks(1:30:181);
yticklabels(["0","30","60","90","120","150","180"]);
a = get(gca,'YTickLabel');  
set(gca,'YTickLabel',a,'fontsize',11,'FontWeight','bold')

xticks(1:30:181);
xticklabels(["0","30","60","90","120","150","180"]);
a = get(gca,'XTickLabel');  
set(gca,'XTickLabel',a,'fontsize',11,'FontWeight','bold')

xline(31,LineWidth=1,LineStyle="--",Color=[0.8 0.8 0.8]);
xline(61,LineWidth=1,LineStyle="--",Color=[0.8 0.8 0.8]);
xline(91,LineWidth=1,LineStyle="--",Color=[0.8 0.8 0.8]);
xline(121,LineWidth=1,LineStyle="--",Color=[0.8 0.8 0.8]);
xline(151,LineWidth=1,LineStyle="--",Color=[0.8 0.8 0.8]);

yline(31,LineWidth=1,LineStyle="--",Color=[0.8 0.8 0.8]);
yline(61,LineWidth=1,LineStyle="--",Color=[0.8 0.8 0.8]);
yline(91,LineWidth=1,LineStyle="--",Color=[0.8 0.8 0.8]);

xlabel("Spatial parameter (degree)","FontSize",13,"FontName","arial","FontWeight","bold");
ylabel("Temporal parameter (rad)","FontSize",13,"FontName","arial","FontWeight","bold");
% clim(fixed_c_axis);

%%
figure; hAxes = gca;
contourf(U_map_mat);

pbaspect([1 1 0.8]);

colormap jet;
colorbar;

yticks(1:30:181);
yticklabels(["0","30","60","90","120","150","180"]);
a = get(gca,'YTickLabel');  
set(gca,'YTickLabel',a,'fontsize',11,'FontWeight','bold')

xticks(1:30:181);
xticklabels(["0","30","60","90","120","150","180"]);
a = get(gca,'XTickLabel');  
set(gca,'XTickLabel',a,'fontsize',11,'FontWeight','bold')

xline(31,LineWidth=1,LineStyle="--",Color=[0.8 0.8 0.8]);
xline(61,LineWidth=1,LineStyle="--",Color=[0.8 0.8 0.8]);
xline(91,LineWidth=1,LineStyle="--",Color=[0.8 0.8 0.8]);
xline(121,LineWidth=1,LineStyle="--",Color=[0.8 0.8 0.8]);
xline(151,LineWidth=1,LineStyle="--",Color=[0.8 0.8 0.8]);

yline(31,LineWidth=1,LineStyle="--",Color=[0.8 0.8 0.8]);
yline(61,LineWidth=1,LineStyle="--",Color=[0.8 0.8 0.8]);
yline(91,LineWidth=1,LineStyle="--",Color=[0.8 0.8 0.8]);

xlabel("Spatial parameter (degree)","FontSize",13,"FontName","arial","FontWeight","bold");
ylabel("Temporal parameter (rad)","FontSize",13,"FontName","arial","FontWeight","bold");
% clim(fixed_c_axis);

%%
% %%
% figure;
% contourf(rad2deg(Rot_vec_curve(:,:,3)))
% 
% %%
% figure
% contourf(rad2deg(Rot_vec_mat(:,:,3)))
% 
% %% 상관계수 비교
% 
% norm_U_mat = normalize(U_map_mat);
% norm_U_curve = normalize(U_map_curve);
% 
% corr2(norm_U_mat, norm_U_curve)
% 
%% 종료 머리 오리엔테이션
figure;
contourf(rad2deg(Tf_orientation_curve));

%%
figure;
contourf(rad2deg(Tf_orientation_mat));
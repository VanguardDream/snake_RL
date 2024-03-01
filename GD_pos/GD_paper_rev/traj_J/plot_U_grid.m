clc; clear;

%% load

% load U_traj_linear_True_45x45x19x19x59x59x0x0_05_21720_.mat %Serp
% load U_traj_linear_True_45x45x15x15x56_5x28_25x0x0_05_21720_.mat %Slit
% load U_traj_linear_True_45x45x27x27x53x53x45x0_05_21720_.mat %Side
load U_traj_linear_True_15x15x0x0x30x30x90x0_05_21720_.mat %Roll

U_map_curve = U_map;
Rot_vec_curve = Rot_vec;
% Tf_orientation_curve = Tf_orientation;

clear max min Motion_lambda param_coefficient U_map Rot_vec Tf_orientation;

% load U_traj_linear_False_45x45x19x19x59x59x0x0_05_21720_.mat  %Serp
% load U_traj_linear_False_45x45x15x15x56_5x28_25x0x0_05_21720_.mat %Slit
% load U_traj_linear_False_45x45x27x27x53x53x45x0_05_21720_.mat %Side
load U_traj_linear_False_15x15x0x0x30x30x90x0_05_21720_.mat %Roll

U_map_mat = U_map;
Rot_vec_mat = Rot_vec;
Tf_orientation_mat = Tf_orientation;

clear max min Motion_lambda param_coefficient U_map Rot_vec Tf_orientation;

U_map_curve = transpose(U_map_curve);
U_map_mat = transpose(U_map_mat);
%%
U_map_mat = squeeze(U_map_mat);
U_map_curve = squeeze(U_map_curve);

U_map_mat = max(U_map_mat, -1000);
U_map_curve = max(U_map_curve, -1000);
% 
% U_map_mat = min(U_map_mat, 1000);
% U_map_curve = min(U_map_curve, 1000);

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

%%
figure;
contourf(rad2deg(Rot_vec_curve(:,:,3)))

%%
figure
contourf(rad2deg(Rot_vec_mat(:,:,3)))

%% 상관계수 비교

norm_U_mat = normalize(U_map_mat);
norm_U_curve = normalize(U_map_curve);

corr2(norm_U_mat, norm_U_curve)
clc; clear;

%% load
load Slit_curve.mat

U_map_each_curve = U_map;
Rot_vec_curve = Rot_vec;
Tf_orientation_curve = Tf_orientation;

clear max min param_coefficient U_map Rot_vec Tf_orientation;

% load U_traj_linear_each_weak_side_curve.mat
load Slit_03.mat

% load U_traj_linear_each_False_0.3_roll.mat
% load U_traj_linear_each_False_0.5_roll.mat
% load U_traj_linear_each_False_0.7_roll.mat
% load U_traj_linear_each_False_0.9_roll.mat

% load U_traj_linear_each_False_0.3_serp.mat
% load U_traj_linear_each_False_0.5_serp.mat
% load U_traj_linear_each_False_0.7_serp.mat
% load U_traj_linear_each_False_0.9_serp.mat

% load U_traj_linear_each_False_0.3_side.mat
% load U_traj_linear_each_False_0.5_side.mat
% load U_traj_linear_each_False_0.7_side.mat
% load U_traj_linear_each_False_0.9_side.mat

% load U_traj_linear_each_False_0.3_slit.mat
% load U_traj_linear_each_False_0.5_slit.mat
% load U_traj_linear_each_False_0.7_slit.mat
% load U_traj_linear_each_False_0.9_slit.mat

U_map_each_mat = U_map;
Rot_vec_mat = Rot_vec;
Tf_orientation_mat = Tf_orientation;

clear max min param_coefficient U_map Rot_vec Tf_orientation;

% Tf_orientation_curve = transpose(Tf_orientation_curve);
% Tf_orientation_mat = transpose(Tf_orientation_mat);
%% U map 계수 설정
i = 300
% i = 10;
j = -30
% j = -1;
l = -0.05;
% l = 0;
rot = -30
% rot = -0;

if Motion_lambda(7)> 38
    tf = -60;
    Tf_orientation_curve = abs(Tf_orientation_curve) - pi/2;
    Tf_orientation_mat = abs(Tf_orientation_mat) - pi/2;
else
    tf = -60;
end

U_map_curve = i * U_map_each_curve(:,:,1) + j * U_map_each_curve(:,:,2) + l * U_map_each_curve(:,:,3) + rot * abs(Rot_vec_curve(:,:,3)) + tf * abs(Tf_orientation_curve);
U_map_mat = i * U_map_each_mat(:,:,1) + j * U_map_each_mat(:,:,2) + l * U_map_each_mat(:,:,3) + rot * abs(Rot_vec_mat(:,:,3)) + tf * abs(Tf_orientation_mat);

U_map_curve = transpose(U_map_curve);
U_map_mat = transpose(U_map_mat);

%%
U_map_mat = squeeze(U_map_mat);
U_map_curve = squeeze(U_map_curve);
% % 
% U_map_mat = max(U_map_mat, 70);
% U_map_curve = max(U_map_curve, 70);

% U_map_mat = min(U_map_mat, 1500);
% U_map_curve = min(U_map_curve, 1500);
%%
figure; hAxes = gca;
contourf(U_map_curve);

colormap jet;
colorbar;

yticks(0:30:181);
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

yline(30,LineWidth=1,LineStyle="--",Color=[0.8 0.8 0.8]);
yline(60,LineWidth=1,LineStyle="--",Color=[0.8 0.8 0.8]);
yline(90,LineWidth=1,LineStyle="--",Color=[0.8 0.8 0.8]);

xlabel("Spatial parameter (degree)","FontSize",13,"FontName","arial","FontWeight","bold");
ylabel("Temporal parameter (rad)","FontSize",13,"FontName","arial","FontWeight","bold");

pbaspect([6 4 0.8]);

%%
figure; hAxes = gca;
contourf(U_map_mat);

pbaspect([6 4 0.8]);

colormap jet;

yticks(0:30:181);
yticklabels(["0","30","60","90","120","150","180"]);
a = get(gca,'YTickLabel');  
% set(gca,'YTickLabel',a,'fontsize',11,'FontWeight','bold')
% 
xticks(1:30:181);
xticklabels(["0","30","60","90","120","150","180"]);
a = get(gca,'XTickLabel');  
% set(gca,'XTickLabel',a,'fontsize',11,'FontWeight','bold')

xline(31,LineWidth=1,LineStyle="--",Color=[0.8 0.8 0.8]);
xline(61,LineWidth=1,LineStyle="--",Color=[0.8 0.8 0.8]);
xline(91,LineWidth=1,LineStyle="--",Color=[0.8 0.8 0.8]);
xline(121,LineWidth=1,LineStyle="--",Color=[0.8 0.8 0.8]);
xline(151,LineWidth=1,LineStyle="--",Color=[0.8 0.8 0.8]);

yline(30,LineWidth=1,LineStyle="--",Color=[0.8 0.8 0.8]);
yline(60,LineWidth=1,LineStyle="--",Color=[0.8 0.8 0.8]);
yline(90,LineWidth=1,LineStyle="--",Color=[0.8 0.8 0.8]);

% xlabel("Spatial parameter (degree)","FontSize",13,"FontName","arial","FontWeight","bold");
% ylabel("Temporal parameter (rad)","FontSize",13,"FontName","arial","FontWeight","bold");

axis off;

% %
% figure;
% contourf(rad2deg(Rot_vec_curve(:,:,3)))
% 
% %%
% figure
% contourf(rad2deg(Rot_vec_mat(:,:,3)))
% 
% %% 종료 머리 오리엔테이션
% figure;
% contourf(rad2deg(Tf_orientation_curve));
% 
% %%
% figure;
% contourf(rad2deg(Tf_orientation_mat));

%% 상관계수 비교

% U 값의 상관계수
fprintf("%s","U 상관계수")
norm_U_mat = normalize(U_map_mat);
norm_U_curve = normalize(U_map_curve);

corr2(norm_U_mat, norm_U_curve)

% CoM 평균 방위
fprintf("%s","CoM 상관계수")
norm_com_mat = normalize(Rot_vec_mat(:,:,3));
norm_com_curve = normalize(Rot_vec_curve(:,:,3));

corr2(norm_com_mat, norm_com_curve)

%% 가속도 그림과 비교
figure;
contourf(transpose(head_acc))

figure; hAxes = gca;

U_new = U_map_curve - 20 * transpose(head_acc);

contourf(U_new);

colormap jet;
colorbar;

yticks(0:30:181);
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

yline(30,LineWidth=1,LineStyle="--",Color=[0.8 0.8 0.8]);
yline(60,LineWidth=1,LineStyle="--",Color=[0.8 0.8 0.8]);
yline(90,LineWidth=1,LineStyle="--",Color=[0.8 0.8 0.8]);

xlabel("Spatial parameter (degree)","FontSize",13,"FontName","arial","FontWeight","bold");
ylabel("Temporal parameter (rad)","FontSize",13,"FontName","arial","FontWeight","bold");

pbaspect([6 4 0.8]);


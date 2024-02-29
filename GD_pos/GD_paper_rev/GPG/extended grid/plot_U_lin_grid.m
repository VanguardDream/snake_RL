clc; clear;

%% load

% load U_map_fine_grid_True_45x45x15x15x56_5x28_25x0x0_05_21720_.mat
load U_map_fine_grid_True_45x45x27x27x53x53x45x0_05_21720_.mat
U_map_curve = U_map;

clear max min Motion_lambda param_coefficient U_map;

load U_map_fine_grid_True_45x45x19x19x59x59x0x0_05_21720_.mat
U_map_mat = U_map;

clear max min Motion_lambda param_coefficient U_map;

U_map_curve = transpose(U_map_curve);
U_map_mat = transpose(U_map_mat);
%%
U_map_mat = squeeze(U_map_mat);
U_map_curve = squeeze(U_map_curve);

U_map_mat = max(U_map_mat, -3000);
U_map_curve = max(U_map_curve, -3000);

% U_map_mat = min(U_map_mat, 3000);
% U_map_curve = min(U_map_curve, 3000);

%%
figure; hAxes = gca;
contourf(U_map_curve);

pbaspect([1.5 1 0.8]);

colormap jet;
colorbar;

yticks(0:30:120);
yticklabels(["0","30","60","90","120"]);
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

pbaspect([1.5 1 0.8]);

colormap jet;
colorbar;

yticks(0:30:120);
yticklabels(["0","30","60","90","120"]);
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
%% 상관계수 비교

norm_U_mat = normalize(U_map_mat);
norm_U_curve = normalize(U_map_curve);

corr2(norm_U_mat, norm_U_curve)
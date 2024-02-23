clc; clear;

%% load
load Slithering_curve.mat;
U_map_curve = U_map;

clear max min Motion_lambda param_coefficient U_map;

load Slithering_mat.mat;
U_map_mat = U_map;

clear max min Motion_lambda param_coefficient U_map;

%%
U_map_mat = squeeze(U_map_mat);
U_map_curve = squeeze(U_map_curve);

U_map_mat = max(U_map_mat, -2000);
U_map_curve = max(U_map_curve, -2000);

U_map_mat = min(U_map_mat, 2500);
U_map_curve = min(U_map_curve, 2500);

%%
figure; hAxes = gca;
contourf(U_map_curve);

pbaspect([0.8 0.8 0.8]);

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
yline(121,LineWidth=1,LineStyle="--",Color=[0.8 0.8 0.8]);
yline(151,LineWidth=1,LineStyle="--",Color=[0.8 0.8 0.8]);

xlabel("Dorsal spatial (degree)","FontSize",13,"FontName","arial","FontWeight","bold");
ylabel("Lateral spatial (degree)","FontSize",13,"FontName","arial","FontWeight","bold");

%%
figure; hAxes = gca;
contourf(U_map_mat);

pbaspect([0.8 0.8 0.8]);

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
yline(121,LineWidth=1,LineStyle="--",Color=[0.8 0.8 0.8]);
yline(151,LineWidth=1,LineStyle="--",Color=[0.8 0.8 0.8]);

xlabel("Dorsal spatial (degree)","FontSize",13,"FontName","arial","FontWeight","bold");
ylabel("Lateral spatial (degree)","FontSize",13,"FontName","arial","FontWeight","bold");
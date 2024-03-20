clc; clear;
%% loads
% cur = load('Slit_curve.mat');
% a = load('Slit_03.mat');
% b = load('Slit_05.mat');
% c = load('Slit_07.mat');
% d = load('Slit_09.mat');

% cur = load('Side_curve.mat');
% a = load('Side_03.mat');
% b = load('Side_05.mat');
% c = load('Side_07.mat');
% d = load('Side_09.mat');

cur = load('Side_curve.mat');
a = load('Side_0.3.mat');
b = load('Side_0.5.mat');
c = load('Side_0.7.mat');
d = load('Side_0.9.mat');

% cur = load('Roll_curve.mat');
% a = load('Roll_03.mat');
% b = load('Roll_05.mat');
% c = load('Roll_07.mat');
% d = load('Roll_09.mat');
%% U 값 계산 X축
% cur
cur_wo_x = cur.head_acc_wo_g(:,:,1);
cur_dist = cur.U_map(:,:,1);
cur_x_dist = cos(cur.Tf_orientation) .* cur_dist;
cur_rot = sqrt( cur.Rot_vec(:,:,1).^2 + cur.Rot_vec(:,:,2).^2 + cur.Rot_vec(:,:,3).^2 );
cur_data = cur_wo_x + 1.5 * cur_x_dist - 0.2 * cur_rot;
% a
a_wo_x = a.head_acc_wo_g(:,:,1);
a_dist = a.U_map(:,:,1);
a_x_dist = cos(a.Tf_orientation) .* a_dist;
a_rot = sqrt( a.Rot_vec(:,:,1).^2 + a.Rot_vec(:,:,2).^2 + a.Rot_vec(:,:,3).^2 );
a_data = a_wo_x + 1.5 * a_x_dist - 0.2 * a_rot;
% b
b_wo_x = b.head_acc_wo_g(:,:,1);
b_dist = b.U_map(:,:,1);
b_x_dist = cos(b.Tf_orientation) .* b_dist;
b_rot = sqrt( b.Rot_vec(:,:,1).^2 + b.Rot_vec(:,:,2).^2 + b.Rot_vec(:,:,3).^2 );
b_data = b_wo_x + 1.5 * b_x_dist - 0.2 * b_rot;
% c
c_wo_x = c.head_acc_wo_g(:,:,1);
c_dist = c.U_map(:,:,1);
c_x_dist = cos(c.Tf_orientation) .* c_dist;
c_rot = sqrt( c.Rot_vec(:,:,1).^2 + c.Rot_vec(:,:,2).^2 + c.Rot_vec(:,:,3).^2 );
c_data = c_wo_x + 1.5 * c_x_dist - 0.2 * c_rot;
% d
d_wo_x = d.head_acc_wo_g(:,:,1);
d_dist = d.U_map(:,:,1);
d_x_dist = cos(d.Tf_orientation) .* d_dist;
d_rot = sqrt( d.Rot_vec(:,:,1).^2 + d.Rot_vec(:,:,2).^2 + d.Rot_vec(:,:,3).^2 );
d_data = d_wo_x + 1.5 * d_x_dist - 0.2 * d_rot;

%% U 값 계산 Y축
% cur
cur_wo_x = cur.head_acc_wo_g(:,:,2);
cur_dist = cur.U_map(:,:,1);
cur_x_dist = sin(cur.Tf_orientation) .* cur_dist;
cur_rot = sqrt( cur.Rot_vec(:,:,1).^2 + cur.Rot_vec(:,:,2).^2 + cur.Rot_vec(:,:,3).^2 );
cur_data = cur_wo_x + 1.5 * cur_x_dist - 0.2 * cur_rot;
% a
a_wo_x = a.head_acc_wo_g(:,:,2);
a_dist = a.U_map(:,:,1);
a_x_dist = sin(a.Tf_orientation) .* a_dist;
a_rot = sqrt( a.Rot_vec(:,:,1).^2 + a.Rot_vec(:,:,2).^2 + a.Rot_vec(:,:,3).^2 );
a_data = a_wo_x + 1.5 * a_x_dist - 0.2 * a_rot;
% b
b_wo_x = b.head_acc_wo_g(:,:,2);
b_dist = b.U_map(:,:,1);
b_x_dist = sin(b.Tf_orientation) .* b_dist;
b_rot = sqrt( b.Rot_vec(:,:,1).^2 + b.Rot_vec(:,:,2).^2 + b.Rot_vec(:,:,3).^2 );
b_data = b_wo_x + 1.5 * b_x_dist - 0.2 * b_rot;
% c
c_wo_x = c.head_acc_wo_g(:,:,2);
c_dist = c.U_map(:,:,1);
c_x_dist = sin(c.Tf_orientation) .* c_dist;
c_rot = sqrt( c.Rot_vec(:,:,1).^2 + c.Rot_vec(:,:,2).^2 + c.Rot_vec(:,:,3).^2 );
c_data = c_wo_x + 1.5 * c_x_dist - 0.2 * c_rot;
% d
d_wo_x = d.head_acc_wo_g(:,:,2);
d_dist = d.U_map(:,:,1);
d_x_dist = sin(d.Tf_orientation) .* d_dist;
d_rot = sqrt( d.Rot_vec(:,:,1).^2 + d.Rot_vec(:,:,2).^2 + d.Rot_vec(:,:,3).^2 );
d_data = d_wo_x + 1.5 * d_x_dist - 0.2 * d_rot;
%%
figure; hAxes = gca;
contourf(cur_data',15);

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

%a
figure; hAxes = gca;
contourf(a_data',15);

colormap jet;
% colorbar;

yticks(0:30:181);
yticklabels(["0","30","60","90","120","150","180"]);
a = get(gca,'YTickLabel');  
% set(gca,'YTickLabel',a,'fontsize',11,'FontWeight','bold')

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

pbaspect([6 4 0.8]);

%b
figure; hAxes = gca;
contourf(b_data',15);

colormap jet;
% colorbar;

yticks(0:30:181);
yticklabels(["0","30","60","90","120","150","180"]);
a = get(gca,'YTickLabel');  
% set(gca,'YTickLabel',a,'fontsize',11,'FontWeight','bold')

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

pbaspect([6 4 0.8]);

%c
figure; hAxes = gca;
contourf(c_data',15);

colormap jet;
% colorbar;

yticks(0:30:181);
yticklabels(["0","30","60","90","120","150","180"]);
a = get(gca,'YTickLabel');  
% set(gca,'YTickLabel',a,'fontsize',11,'FontWeight','bold')

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

pbaspect([6 4 0.8]);

%d
figure; hAxes = gca;
contourf(d_data',15);

colormap jet;
% colorbar;

yticks(0:30:181);
yticklabels(["0","30","60","90","120","150","180"]);
a = get(gca,'YTickLabel');  
% set(gca,'YTickLabel',a,'fontsize',11,'FontWeight','bold')

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

pbaspect([6 4 0.8]);

%% 상관계수
corr2(a_data,cur_data)
corr2(b_data,cur_data)
corr2(c_data,cur_data)
corr2(d_data,cur_data)


%% Y축
% 
% figure
% 
% acc_wo_y = head_acc_wo_g(:,:,2);
% dist = U_map(:,:,1);
% y_dist = abs(sin(Tf_orientation) .* dist);
% rot = sqrt(Rot_vec(:,:,1).^2 + Rot_vec(:,:,2).^2 + Rot_vec(:,:,3).^2);
% 
% data = 1.0 * acc_wo_y + 1.5 * y_dist - 0.2 * rot;
% 
% contourf(transpose(data),15)
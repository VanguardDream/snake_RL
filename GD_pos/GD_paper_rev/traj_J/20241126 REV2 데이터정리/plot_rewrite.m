clc; clear;
%% loads
load('Slit_c.mat');


% cur = load('Side_curve.mat');
% a = load('Side_03.mat');
% b = load('Side_05.mat');
% c = load('Side_07.mat');
% d = load('Side_09.mat');

% cur = load('Side_curve.mat');
% a = load('Side_0.3.mat');
% b = load('Side_0.5.mat');
% c = load('Side_0.7.mat');
% d = load('Side_0.9.mat');

% cur = load('Roll_curve.mat');
% a = load('Roll_03.mat');
% b = load('Roll_05.mat');
% c = load('Roll_07.mat');
% d = load('Roll_09.mat');
%% U 값 계산 Curr_plot 파일 기반으로
c_acc = head_acc_wo_g;
c_dist = U_map(:,:,1);
c_rot = sqrt(Rot_vec(:,:,1).^2 + Rot_vec(:,:,2).^2 + Rot_vec(:,:,3).^2);
c_tf = Tf_orientation;

if Motion_lambda(7) > 38
    m_side = true;
else
    m_side = false;
end

if Motion_lambda(7) > 38
    c_side = true;
else
    c_side = false;
end

if c_side
    c_forward_dist = (sin(c_tf) .* c_dist);
    c_forward_acc = c_acc(:,:,2);
    % c_forward_acc = 0;
else
    c_forward_dist = cos(c_tf) .* c_dist;
    c_forward_acc = c_acc(:,:,1);
end

c_data = 1.0 * c_forward_acc + 1.5 * c_forward_dist - 0.2 * c_rot;

c_data = transpose(c_data);

%%
figure; hAxes = gca;
% contourf(cur_data',15);
contourf(c_data,15);

colormap bone;
% colorbar;

yticks(0:30:181);
yticklabels(["0","30","60","90","120","150","180"]);
a = get(gca,'YTickLabel');  
set(gca,'YTickLabel',a,'fontsize',11,'FontWeight','bold')

xticks(1:30:181);
xticklabels(["0","30","60","90","120","150","180"]);
a = get(gca,'XTickLabel');  
set(gca,'XTickLabel',a,'fontsize',11,'FontWeight','bold')

xline(31,LineWidth=1,LineStyle="--",Color=[0.9 0.9 0.9]);
xline(61,LineWidth=1,LineStyle="--",Color=[0.9 0.9 0.9]);
xline(91,LineWidth=1,LineStyle="--",Color=[0.9 0.9 0.9]);
xline(121,LineWidth=1,LineStyle="--",Color=[0.9 0.9 0.9]);
xline(151,LineWidth=1,LineStyle="--",Color=[0.9 0.9 0.9]);

yline(30,LineWidth=1,LineStyle="--",Color=[0.9 0.9 0.9]);
yline(60,LineWidth=1,LineStyle="--",Color=[0.9 0.9 0.9]);
yline(90,LineWidth=1,LineStyle="--",Color=[0.9 0.9 0.9]);

xlabel("Spatial parameter ( a )","FontSize",13,"FontName","arial","FontWeight","bold");
ylabel("Temporal parameter (  a  )","FontSize",13,"FontName","arial","FontWeight","bold");

pbaspect([2 1 0.8]);
box on;
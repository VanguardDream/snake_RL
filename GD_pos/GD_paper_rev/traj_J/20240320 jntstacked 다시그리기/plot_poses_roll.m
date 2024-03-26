clc; clear;
%%
% load side_data.mat;
load slit_acc_data.mat;
% load roll_acc_data.mat;

slit_curve = slit_curve(1:10:end,:);
slit_03 = slit_03(1:10:end,:);
slit_05 = slit_05(1:10:end,:);
slit_07 = slit_07(1:10:end,:);
slit_09 = slit_09(1:10:end,:);

%%
figure;
hold on;
% plot(slit_curve(1:41,1),LineWidth=1.5,LineStyle=":",Color=[0.1 0.1 0.1])
% plot(slit_03(1:41,1),LineWidth=1.5,LineStyle="-",Color=[0.3 0.3 0.3])
% plot(slit_05(1:41,1),LineWidth=1.5,LineStyle=":",Color=[0.5 0.5 0.5])
% plot(slit_07(1:41,1),LineWidth=1.5,LineStyle="-.",Color=[0.5 0.5 0.5])
% plot(slit_09(1:41,1),LineWidth=1.5,LineStyle="-",Color=[0.7 0.7 0.7])

% [“#1984c5”, "#22a7f0”, “#63bff0”, “#a7d5ed”, “#e2e2e2”, “#e1a692”, “#de6e56”, “#e14b31”, “#c23728”]
p1 = plot(slit_curve(1:46,1),LineWidth=1.5,LineStyle=":",Color=[0.1 0.1 0.1]); p1.Color(4) = 0.7;
p2 = plot(slit_03(1:46,1),LineWidth=1.5,LineStyle="-",Color="#000080"); p2.Color(4) = 0.7;
p3 = plot(slit_05(1:46,1),LineWidth=1.5,LineStyle="--",Color="#004d00"); p3.Color(4) = 0.7;
p4 = plot(slit_07(1:46,1),LineWidth=1.5,LineStyle="-",Color="#800020"); p4.Color(4) = 0.7;
p5 = plot(slit_09(1:46,1),LineWidth=1.5,LineStyle="--",Color="#B8860B"); p5.Color(4) = 0.7;

legend({"Serpenoid", "gamma = 0.3", "gamma = 0.5", "gamma = 0.7", "gamma = 0.9"},'NumColumns',3,FontSize=9,FontName='arial',Location='northwest',Fontweight='bold');

t = 1:5:200;
xticks(t);
xticklabels((t-1)*0.05);
xlim([1 41]);
% a = get(gca,'YTickLabel');  
% set(gca,'YTickLabel',a,'fontsize',11,'FontWeight','bold')

pos = -pi/3:pi/6:pi/2;
yticks(pos);
yticklabels({"-\pi/3", "-\pi/6", "0", "\pi/6", "\pi/3", "\pi/2"});
ylim([-pi/5.9999 pi/2.999]);
% a = get(gca,'XTickLabel');  
% set(gca,'XTickLabel',a,'fontsize',11,'FontWeight','bold')

ax = gca;
X = ax.XAxis;
Y = ax.YAxis;
X.FontSize = 11;
Y.FontSize = 11;
X.FontName = 'arial';
Y.FontName = 'arial';
X.FontWeight = 'bold';
Y.FontWeight = 'bold';

grid on;
% 
grid_ax = gca;
grid_ax.LineWidth = 1;
grid_ax.GridLineStyle = "--";
grid_ax.GridColor = [0.2 0.2 0.2];
% grid_ax.YGrid = "off";

xlabel("Time (sec)","FontSize",13,"FontName","arial","FontWeight","bold");
ylabel("Dorsal joint input (rad)","FontSize",13,"FontName","arial","FontWeight","bold");

pbaspect([2 0.8 0.8]);
clear a;

%%
figure;
hold on;
% plot(slit_curve(1:41,1),LineWidth=1.5,LineStyle=":",Color=[0.1 0.1 0.1])
% plot(slit_03(1:41,1),LineWidth=1.5,LineStyle="-",Color=[0.3 0.3 0.3])
% plot(slit_05(1:41,1),LineWidth=1.5,LineStyle=":",Color=[0.5 0.5 0.5])
% plot(slit_07(1:41,1),LineWidth=1.5,LineStyle="-.",Color=[0.5 0.5 0.5])
% plot(slit_09(1:41,1),LineWidth=1.5,LineStyle="-",Color=[0.7 0.7 0.7])

% [“#1984c5”, "#22a7f0”, “#63bff0”, “#a7d5ed”, “#e2e2e2”, “#e1a692”, “#de6e56”, “#e14b31”, “#c23728”]
p1 = plot(slit_curve(1:46,2),LineWidth=1.5,LineStyle=":",Color=[0.1 0.1 0.1]); p1.Color(4) = 0.7;
p2 = plot(slit_03(1:46,2),LineWidth=1.5,LineStyle="-",Color="#000080"); p2.Color(4) = 0.7;
p3 = plot(slit_05(1:46,2),LineWidth=1.5,LineStyle="--",Color="#004d00"); p3.Color(4) = 0.7;
p4 = plot(slit_07(1:46,2),LineWidth=1.5,LineStyle="-",Color="#800020"); p4.Color(4) = 0.7;
p5 = plot(slit_09(1:46,2),LineWidth=1.5,LineStyle="--",Color="#B8860B"); p5.Color(4) = 0.7;

legend({"Serpenoid", "gamma = 0.3", "gamma = 0.5", "gamma = 0.7", "gamma = 0.9"},'NumColumns',3,FontSize=9,FontName='arial',Location='northwest',Fontweight='bold');

t = 1:5:200;
xticks(t);
xticklabels((t-1)*0.05);
xlim([1 41]);
% a = get(gca,'YTickLabel');  
% set(gca,'YTickLabel',a,'fontsize',11,'FontWeight','bold')

pos = -pi/3:pi/6:pi/2;
yticks(pos);
yticklabels({"-\pi/3", "-\pi/6", "0", "\pi/6", "\pi/3", "\pi/2"});
ylim([-pi/5.9999 pi/2.999]);
% a = get(gca,'XTickLabel');  
% set(gca,'XTickLabel',a,'fontsize',11,'FontWeight','bold')

ax = gca;
X = ax.XAxis;
Y = ax.YAxis;
X.FontSize = 11;
Y.FontSize = 11;
X.FontName = 'arial';
Y.FontName = 'arial';
X.FontWeight = 'bold';
Y.FontWeight = 'bold';

grid on;
% 
grid_ax = gca;
grid_ax.LineWidth = 1;
grid_ax.GridLineStyle = "--";
grid_ax.GridColor = [0.2 0.2 0.2];
% grid_ax.YGrid = "off";

xlabel("Time (sec)","FontSize",13,"FontName","arial","FontWeight","bold");
ylabel("Lateral joint input (rad)","FontSize",13,"FontName","arial","FontWeight","bold");

pbaspect([2 0.8 0.8]);
clear a;

%%
figure;

hold on;
% plot(tra_curve(:,1),tra_curve(:,2));
% plot(tra_03(:,1),tra_03(:,2));
% plot(tra_05(:,1),tra_05(:,2));
% plot(tra_07(:,1),tra_07(:,2));
% plot(tra_09(:,1),tra_09(:,2));

p1 = plot(tra_curve(:,1),tra_curve(:,2),LineWidth=1.5,LineStyle=":",Color=[0.1 0.1 0.1]); p1.Color(4) = 0.7;
p2 = plot(tra_03(:,1),tra_03(:,2),LineWidth=1.5,LineStyle="-",Color="#000080"); p2.Color(4) = 0.7;
p3 = plot(tra_05(:,1),tra_05(:,2),LineWidth=1.5,LineStyle="-",Color="#004d00"); p3.Color(4) = 0.7;
p4 = plot(tra_07(:,1),tra_07(:,2),LineWidth=1.5,LineStyle="-",Color="#800020"); p4.Color(4) = 0.7;
p5 = plot(tra_09(:,1),tra_09(:,2),LineWidth=1.5,LineStyle="-",Color="#B8860B"); p5.Color(4) = 0.7;

rad_curve = norm(tra_curve(end,:));
rad_03 = norm(tra_03(end,:));
rad_05 = norm(tra_05(end,:));
rad_07 = norm(tra_07(end,:));
rad_09 = norm(tra_09(end,:));
theta = linspace(0, 2*pi, 3000);

x=rad_07*cos(theta);y=rad_07*sin(theta);plot(x,y,LineWidth=1,LineStyle="-.",Color=[0.1 0.1 0.1 0.8])
x=rad_09*cos(theta);y=rad_09*sin(theta);plot(x,y,LineWidth=1,LineStyle=":",Color=[0.1 0.1 0.1 0.8])
% x=rad_03*cos(theta);y=rad_03*sin(theta);plot(x,y)
% x=rad_05*cos(theta);y=rad_05*sin(theta);plot(x,y)
% x=rad_07*cos(theta);y=rad_07*sin(theta);plot(x,y)
% x=rad_09*cos(theta);y=rad_09*sin(theta);plot(x,y)

plot(tra_curve(end,1),tra_curve(end,2),Marker="o",MarkerSize=5,MarkerEdgeColor=[0.8 0.8 0.8],MarkerFaceColor=[0.1 0.1 0.1]);
plot(tra_03(end,1),tra_03(end,2),Marker="o",MarkerSize=5,MarkerEdgeColor=[0.8 0.8 0.8],MarkerFaceColor="#000080");
plot(tra_05(end,1),tra_05(end,2),Marker="o",MarkerSize=5,MarkerEdgeColor=[0.8 0.8 0.8],MarkerFaceColor="#004d00");
plot(tra_07(end,1),tra_07(end,2),Marker="o",MarkerSize=5,MarkerEdgeColor=[0.8 0.8 0.8],MarkerFaceColor="#800020");
plot(tra_09(end,1),tra_09(end,2),Marker="o",MarkerSize=5,MarkerEdgeColor=[0.8 0.8 0.8],MarkerFaceColor="#B8860B");

legend({"Serpenoid", "gamma = 0.3", "gamma = 0.5", "gamma = 0.7", "gamma = 0.9"},'NumColumns',2,FontSize=9,FontName='arial',Location='southwest',Fontweight='bold');

ax = gca;
X = ax.XAxis;
Y = ax.YAxis;
X.FontSize = 11;
Y.FontSize = 11;
X.FontName = 'arial';
Y.FontName = 'arial';
X.FontWeight = 'bold';
Y.FontWeight = 'bold';

default_x = [-1.75 1.75];
default_y = [-1 1];

xlim(default_x + 0.75)
ylim(default_y + 0.2)

grid on;
grid_ax = gca;
grid_ax.LineWidth = 1;
grid_ax.GridLineStyle = "--";
grid_ax.GridColor = [0.2 0.2 0.2];
grid_ax.Color = '#FEF9D7';

pbaspect([sum(abs(default_x)) sum(abs(default_y)) 0.8]);

xlabel("x (m)","FontSize",13,"FontName","arial","FontWeight","bold");
ylabel("y (m)","FontSize",13,"FontName","arial","FontWeight","bold");

%%
figure;

hold on;
% r_tra_curve = [tra_curve(:,1) -tra_curve(:,2)];
% r_tra_03 = [tra_03(:,1) -tra_03(:,2)];
% r_tra_05 = [tra_05(:,1) -tra_05(:,2)];
% r_tra_07 = [tra_07(:,1) -tra_07(:,2)];
% r_tra_09 = [tra_09(:,1) -tra_09(:,2)];

r_tra_curve = [tra_curve(:,1) tra_curve(:,2)];
r_tra_03 = [tra_03(:,1) tra_03(:,2)];
r_tra_05 = [tra_05(:,1) tra_05(:,2)];
r_tra_07 = [tra_07(:,1) tra_07(:,2)];
r_tra_09 = [tra_09(:,1) tra_09(:,2)];

p1 = plot(r_tra_curve(:,2),r_tra_curve(:,1),LineWidth=1.5,LineStyle=":",Color=[0.1 0.1 0.1]); p1.Color(4) = 0.7;
p2 = plot(r_tra_03(:,2),r_tra_03(:,1),LineWidth=1.5,LineStyle="-",Color="#000080"); p2.Color(4) = 0.7;
p3 = plot(r_tra_05(:,2),r_tra_05(:,1),LineWidth=1.5,LineStyle="-",Color="#004d00"); p3.Color(4) = 0.7;
p4 = plot(r_tra_07(:,2),r_tra_07(:,1),LineWidth=1.5,LineStyle="-",Color="#800020"); p4.Color(4) = 0.7;
p5 = plot(r_tra_09(:,2),r_tra_09(:,1),LineWidth=1.5,LineStyle="-",Color="#B8860B"); p5.Color(4) = 0.7;

rad_curve = norm(r_tra_curve(end,:));
rad_03 = norm(r_tra_03(end,:));
rad_05 = norm(r_tra_05(end,:));
rad_07 = norm(r_tra_07(end,:));
rad_09 = norm(r_tra_09(end,:));
theta = linspace(0, 2*pi, 3000);

x=rad_05*cos(theta);y=rad_05*sin(theta);plot(x,y,LineWidth=1,LineStyle="-.",Color=[0.1 0.1 0.1 0.8])
x=rad_09*cos(theta);y=rad_09*sin(theta);plot(x,y,LineWidth=1,LineStyle=":",Color=[0.1 0.1 0.1 0.8])
% x=rad_03*cos(theta);y=rad_03*sin(theta);plot(x,y)
% x=rad_05*cos(theta);y=rad_05*sin(theta);plot(x,y)
% x=rad_07*cos(theta);y=rad_07*sin(theta);plot(x,y)
% x=rad_09*cos(theta);y=rad_09*sin(theta);plot(x,y)

plot(r_tra_curve(end,2),r_tra_curve(end,1),Marker="o",MarkerSize=5,MarkerEdgeColor=[0.8 0.8 0.8],MarkerFaceColor=[0.1 0.1 0.1]);
plot(r_tra_03(end,2),r_tra_03(end,1),Marker="o",MarkerSize=5,MarkerEdgeColor=[0.8 0.8 0.8],MarkerFaceColor="#000080");
plot(r_tra_05(end,2),r_tra_05(end,1),Marker="o",MarkerSize=5,MarkerEdgeColor=[0.8 0.8 0.8],MarkerFaceColor="#004d00");
plot(r_tra_07(end,2),r_tra_07(end,1),Marker="o",MarkerSize=5,MarkerEdgeColor=[0.8 0.8 0.8],MarkerFaceColor="#800020");
plot(r_tra_09(end,2),r_tra_09(end,1),Marker="o",MarkerSize=5,MarkerEdgeColor=[0.8 0.8 0.8],MarkerFaceColor="#B8860B");

legend({"Serpenoid", "gamma = 0.3", "gamma = 0.5", "gamma = 0.7", "gamma = 0.9"},'NumColumns',2,FontSize=9,FontName='arial',Location='northwest',Fontweight='bold');
% 
% xticks(-9:1:9);
% yticks(-9:0.5:9);

ax = gca;
X = ax.XAxis;
Y = ax.YAxis;
X.FontSize = 11;
Y.FontSize = 11;
X.FontName = 'arial';
Y.FontName = 'arial';
X.FontWeight = 'bold';
Y.FontWeight = 'bold';

xtickformat('%.1f')
ytickformat('%.1f')

g_ratio = 0.78;

default_x = [-1 * 7 * g_ratio /2, 7 * g_ratio /2];
default_y = [-1 * 4 * g_ratio /2, 4 * g_ratio /2];

xlim(default_x + 1.50)
ylim(default_y - 0.20)

grid on;
grid_ax = gca;
grid_ax.LineWidth = 1;
grid_ax.GridLineStyle = "--";
grid_ax.GridColor = [0.2 0.2 0.2];
grid_ax.Color = '#FEF9D7';

pbaspect([sum(abs(default_x)) sum(abs(default_y)) 0.8]);
% pbaspect([3.5 2 0.8]);

xlabel("y (m)","FontSize",13,"FontName","arial","FontWeight","bold");
ylabel("x (m)","FontSize",13,"FontName","arial","FontWeight","bold");
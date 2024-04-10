clc;clear;
%% load side
load side_curve_2.mat
slit_curve = position;
slit_curve = deg2rad(slit_curve);
rpm_curve = velocity;
tor_curve = current;
clear position current gait velocity gamma

load side_3_2.mat
slit_03 = position;
slit_03 = deg2rad(slit_03);
rpm_03 = velocity;
tor_03 = current;
clear position current gait velocity gamma

load side_5_2.mat
slit_05 = position;
slit_05 = deg2rad(slit_05);
rpm_05 = velocity;
tor_05 = current;
clear position current gait velocity gamma

load side_7_2.mat
slit_07 = position;
slit_07 = deg2rad(slit_07);
rpm_07 = velocity;
tor_07 = current;
clear position current gait velocity gamma

load side_9_3.mat
slit_09 = position;
slit_09 = deg2rad(slit_09);
rpm_09 = velocity;
tor_09 = current;
clear position current gait velocity gamma

%% Dorsal Position
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
ylim([-pi/2.9999 pi/2.099]);
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
ax.Color = '#f3f4fe';

grid on;
% 
grid_ax = gca;
grid_ax.LineWidth = 1;
grid_ax.GridLineStyle = "--";
grid_ax.GridColor = [0.2 0.2 0.2];
% grid_ax.YGrid = "off";

xlabel("Time (sec)","FontSize",13,"FontName","arial","FontWeight","bold");
ylabel("Dorsal joint position (rad)","FontSize",13,"FontName","arial","FontWeight","bold");

pbaspect([2 0.8 0.8]);
clear a;

%% Lateral Position
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
ylim([-pi/2.9999 pi/2.099]);
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
ax.Color = '#f3f4fe';

grid on;
% 
grid_ax = gca;
grid_ax.LineWidth = 1;
grid_ax.GridLineStyle = "--";
grid_ax.GridColor = [0.2 0.2 0.2];
% grid_ax.YGrid = "off";

xlabel("Time (sec)","FontSize",13,"FontName","arial","FontWeight","bold");
ylabel("Lateral joint position (rad)","FontSize",13,"FontName","arial","FontWeight","bold");

pbaspect([2 0.8 0.8]);
clear a;

%% Dor Vel
figure;
hold on;
% plot(slit_curve(1:41,1),LineWidth=1.5,LineStyle=":",Color=[0.1 0.1 0.1])
% plot(slit_03(1:41,1),LineWidth=1.5,LineStyle="-",Color=[0.3 0.3 0.3])
% plot(slit_05(1:41,1),LineWidth=1.5,LineStyle=":",Color=[0.5 0.5 0.5])
% plot(slit_07(1:41,1),LineWidth=1.5,LineStyle="-.",Color=[0.5 0.5 0.5])
% plot(slit_09(1:41,1),LineWidth=1.5,LineStyle="-",Color=[0.7 0.7 0.7])

% [“#1984c5”, "#22a7f0”, “#63bff0”, “#a7d5ed”, “#e2e2e2”, “#e1a692”, “#de6e56”, “#e14b31”, “#c23728”]
p1 = plot(rpm_curve(1:46,1),LineWidth=1.5,LineStyle=":",Color=[0.1 0.1 0.1]); p1.Color(4) = 0.7;
p2 = plot(rpm_03(1:46,1),LineWidth=1.5,LineStyle="-",Color="#000080"); p2.Color(4) = 0.7;
p3 = plot(rpm_05(1:46,1),LineWidth=1.5,LineStyle="--",Color="#004d00"); p3.Color(4) = 0.7;
p4 = plot(rpm_07(1:46,1),LineWidth=1.5,LineStyle="-",Color="#800020"); p4.Color(4) = 0.7;
p5 = plot(rpm_09(1:46,1),LineWidth=1.5,LineStyle="--",Color="#B8860B"); p5.Color(4) = 0.7;

legend({"Serpenoid", "gamma = 0.3", "gamma = 0.5", "gamma = 0.7", "gamma = 0.9"},'NumColumns',3,FontSize=9,FontName='arial',Location='northwest',Fontweight='bold');

t = 1:5:200;
xticks(t);
xticklabels((t-1)*0.05);
xlim([1 41]);
% a = get(gca,'YTickLabel');  
% set(gca,'YTickLabel',a,'fontsize',11,'FontWeight','bold')

vel = -80:20:100;
yticks(vel);
% yticklabels({"-\pi/3", "-\pi/6", "0", "\pi/6", "\pi/3", "\pi/2"});
ylim([-70 100]);
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
ax.Color = '#f6fef5';

grid on;
% 
grid_ax = gca;
grid_ax.LineWidth = 1;
grid_ax.GridLineStyle = "--";
grid_ax.GridColor = [0.2 0.2 0.2];
% grid_ax.YGrid = "off";

xlabel("Time (sec)","FontSize",13,"FontName","arial","FontWeight","bold");
ylabel("Dorsal joint velocity (RPM)","FontSize",13,"FontName","arial","FontWeight","bold");

pbaspect([2 0.8 0.8]);
clear a;

%% Lat Vel
figure;
hold on;
% plot(slit_curve(1:41,1),LineWidth=1.5,LineStyle=":",Color=[0.1 0.1 0.1])
% plot(slit_03(1:41,1),LineWidth=1.5,LineStyle="-",Color=[0.3 0.3 0.3])
% plot(slit_05(1:41,1),LineWidth=1.5,LineStyle=":",Color=[0.5 0.5 0.5])
% plot(slit_07(1:41,1),LineWidth=1.5,LineStyle="-.",Color=[0.5 0.5 0.5])
% plot(slit_09(1:41,1),LineWidth=1.5,LineStyle="-",Color=[0.7 0.7 0.7])

% [“#1984c5”, "#22a7f0”, “#63bff0”, “#a7d5ed”, “#e2e2e2”, “#e1a692”, “#de6e56”, “#e14b31”, “#c23728”]
p1 = plot(rpm_curve(1:46,2),LineWidth=1.5,LineStyle=":",Color=[0.1 0.1 0.1]); p1.Color(4) = 0.7;
p2 = plot(rpm_03(1:46,2),LineWidth=1.5,LineStyle="-",Color="#000080"); p2.Color(4) = 0.7;
p3 = plot(rpm_05(1:46,2),LineWidth=1.5,LineStyle="--",Color="#004d00"); p3.Color(4) = 0.7;
p4 = plot(rpm_07(1:46,2),LineWidth=1.5,LineStyle="-",Color="#800020"); p4.Color(4) = 0.7;
p5 = plot(rpm_09(1:46,2),LineWidth=1.5,LineStyle="--",Color="#B8860B"); p5.Color(4) = 0.7;

legend({"Serpenoid", "gamma = 0.3", "gamma = 0.5", "gamma = 0.7", "gamma = 0.9"},'NumColumns',3,FontSize=9,FontName='arial',Location='northwest',Fontweight='bold');

t = 1:5:200;
xticks(t);
xticklabels((t-1)*0.05);
xlim([1 41]);
% a = get(gca,'YTickLabel');  
% set(gca,'YTickLabel',a,'fontsize',11,'FontWeight','bold')

vel = -80:20:100;
yticks(vel);
% yticklabels({"-\pi/3", "-\pi/6", "0", "\pi/6", "\pi/3", "\pi/2"});
ylim([-70 100]);
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
ax.Color = '#f6fef5';

grid on;
% 
grid_ax = gca;
grid_ax.LineWidth = 1;
grid_ax.GridLineStyle = "--";
grid_ax.GridColor = [0.2 0.2 0.2];
% grid_ax.YGrid = "off";

xlabel("Time (sec)","FontSize",13,"FontName","arial","FontWeight","bold");
ylabel("Lateral joint velocity (RPM)","FontSize",13,"FontName","arial","FontWeight","bold");

pbaspect([2 0.8 0.8]);
clear a;
%% Dor Cur
figure;
hold on;
% plot(slit_curve(1:41,1),LineWidth=1.5,LineStyle=":",Color=[0.1 0.1 0.1])
% plot(slit_03(1:41,1),LineWidth=1.5,LineStyle="-",Color=[0.3 0.3 0.3])
% plot(slit_05(1:41,1),LineWidth=1.5,LineStyle=":",Color=[0.5 0.5 0.5])
% plot(slit_07(1:41,1),LineWidth=1.5,LineStyle="-.",Color=[0.5 0.5 0.5])
% plot(slit_09(1:41,1),LineWidth=1.5,LineStyle="-",Color=[0.7 0.7 0.7])

% [“#1984c5”, "#22a7f0”, “#63bff0”, “#a7d5ed”, “#e2e2e2”, “#e1a692”, “#de6e56”, “#e14b31”, “#c23728”]
p1 = plot(tor_curve(1:46,1),LineWidth=1.5,LineStyle=":",Color=[0.1 0.1 0.1]); p1.Color(4) = 0.7;
p2 = plot(tor_03(1:46,1),LineWidth=1.5,LineStyle="-",Color="#000080"); p2.Color(4) = 0.7;
p3 = plot(tor_05(1:46,1),LineWidth=1.5,LineStyle="--",Color="#004d00"); p3.Color(4) = 0.7;
p4 = plot(tor_07(1:46,1),LineWidth=1.5,LineStyle="-",Color="#800020"); p4.Color(4) = 0.7;
p5 = plot(tor_09(1:46,1),LineWidth=1.5,LineStyle="--",Color="#B8860B"); p5.Color(4) = 0.7;

legend({"Serpenoid", "gamma = 0.3", "gamma = 0.5", "gamma = 0.7", "gamma = 0.9"},'NumColumns',3,FontSize=9,FontName='arial',Location='northwest',Fontweight='bold');

t = 1:5:200;
xticks(t);
xticklabels((t-1)*0.05);
xlim([1 41]);
% a = get(gca,'YTickLabel');  
% set(gca,'YTickLabel',a,'fontsize',11,'FontWeight','bold')

vel = -1100:400:1700;
yticks(vel);
% yticklabels({"-\pi/3", "-\pi/6", "0", "\pi/6", "\pi/3", "\pi/2"});
ylim([-1100 1700]);
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
ax.Color = '#fdf4ec';

grid on;
% 
grid_ax = gca;
grid_ax.LineWidth = 1;
grid_ax.GridLineStyle = "--";
grid_ax.GridColor = [0.2 0.2 0.2];
% grid_ax.YGrid = "off";

xlabel("Time (sec)","FontSize",13,"FontName","arial","FontWeight","bold");
ylabel("Dorsal joint current (mA)","FontSize",13,"FontName","arial","FontWeight","bold");

pbaspect([2 0.8 0.8]);
clear a;
%% Lat Cur
figure;
hold on;
% plot(slit_curve(1:41,1),LineWidth=1.5,LineStyle=":",Color=[0.1 0.1 0.1])
% plot(slit_03(1:41,1),LineWidth=1.5,LineStyle="-",Color=[0.3 0.3 0.3])
% plot(slit_05(1:41,1),LineWidth=1.5,LineStyle=":",Color=[0.5 0.5 0.5])
% plot(slit_07(1:41,1),LineWidth=1.5,LineStyle="-.",Color=[0.5 0.5 0.5])
% plot(slit_09(1:41,1),LineWidth=1.5,LineStyle="-",Color=[0.7 0.7 0.7])

% [“#1984c5”, "#22a7f0”, “#63bff0”, “#a7d5ed”, “#e2e2e2”, “#e1a692”, “#de6e56”, “#e14b31”, “#c23728”]
p1 = plot(tor_curve(1:46,2),LineWidth=1.5,LineStyle=":",Color=[0.1 0.1 0.1]); p1.Color(4) = 0.7;
p2 = plot(tor_03(1:46,2),LineWidth=1.5,LineStyle="-",Color="#000080"); p2.Color(4) = 0.7;
p3 = plot(tor_05(1:46,2),LineWidth=1.5,LineStyle="--",Color="#004d00"); p3.Color(4) = 0.7;
p4 = plot(tor_07(1:46,2),LineWidth=1.5,LineStyle="-",Color="#800020"); p4.Color(4) = 0.7;
p5 = plot(tor_09(1:46,2),LineWidth=1.5,LineStyle="--",Color="#B8860B"); p5.Color(4) = 0.7;

legend({"Serpenoid", "gamma = 0.3", "gamma = 0.5", "gamma = 0.7", "gamma = 0.9"},'NumColumns',3,FontSize=9,FontName='arial',Location='northwest',Fontweight='bold');

t = 1:5:200;
xticks(t);
xticklabels((t-1)*0.05);
xlim([1 41]);
% a = get(gca,'YTickLabel');  
% set(gca,'YTickLabel',a,'fontsize',11,'FontWeight','bold')

vel = -1100:400:1700;
yticks(vel);
% yticklabels({"-\pi/3", "-\pi/6", "0", "\pi/6", "\pi/3", "\pi/2"});
ylim([-1100 1700]);
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
ax.Color = '#fdf4ec';

grid on;
% 
grid_ax = gca;
grid_ax.LineWidth = 1;
grid_ax.GridLineStyle = "--";
grid_ax.GridColor = [0.2 0.2 0.2];
% grid_ax.YGrid = "off";

xlabel("Time (sec)","FontSize",13,"FontName","arial","FontWeight","bold");
ylabel("Lateral joint current (mA)","FontSize",13,"FontName","arial","FontWeight","bold");

pbaspect([2 0.8 0.8]);
clear a;
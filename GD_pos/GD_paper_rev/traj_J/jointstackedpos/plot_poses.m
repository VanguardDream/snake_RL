clc; clear;

%%
load gait_poses.mat

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
plot(slit_curve(1:41,1),LineWidth=1.5,LineStyle=":",Color=[0.1 0.1 0.1])
plot(slit_03(1:41,1),LineWidth=1.5,LineStyle="-",Color="#000080")
plot(slit_05(1:41,1),LineWidth=1.5,LineStyle="--",Color="#004d00")
plot(slit_07(1:41,1),LineWidth=1.5,LineStyle="-",Color="#800020")
plot(slit_09(1:41,1),LineWidth=1.5,LineStyle="--",Color="#B8860B")

legend({"Serpenoid", "gamma = 0.3", "gamma = 0.5", "gamma = 0.7", "gamma = 0.9"},'NumColumns',2,FontSize=9,FontName='arial',Location='northeast');

t = 0:5:200;
xticks(t);
xticklabels(t*0.05);
xlim([0 42]);
a = get(gca,'YTickLabel');  
set(gca,'YTickLabel',a,'fontsize',11,'FontWeight','bold')

pos = -pi/2:pi/6:pi/2;
yticks(pos);
yticklabels({"-\pi/2", "-\pi/3", "-\pi/6", "0", "\pi/6", "\pi/3", "\pi/2"});
ylim([-pi/2.99 pi/2]);
a = get(gca,'XTickLabel');  
set(gca,'XTickLabel',a,'fontsize',11,'FontWeight','bold')

grid on;
% 
grid_ax = gca;
grid_ax.LineWidth = 1;
grid_ax.GridLineStyle = "--";
grid_ax.GridColor = [0.2 0.2 0.2];
% grid_ax.YGrid = "off";

xlabel("Time (sec)","FontSize",13,"FontName","arial","FontWeight","bold");
ylabel("Dorsal joint position (rad)","FontSize",13,"FontName","arial","FontWeight","bold");

pbaspect([2 1.1 0.8]);

%%
figure;
hold on;
% plot(slit_curve(1:41,1),LineWidth=1.5,LineStyle=":",Color=[0.1 0.1 0.1])
% plot(slit_03(1:41,1),LineWidth=1.5,LineStyle="-",Color=[0.3 0.3 0.3])
% plot(slit_05(1:41,1),LineWidth=1.5,LineStyle=":",Color=[0.5 0.5 0.5])
% plot(slit_07(1:41,1),LineWidth=1.5,LineStyle="-.",Color=[0.5 0.5 0.5])
% plot(slit_09(1:41,1),LineWidth=1.5,LineStyle="-",Color=[0.7 0.7 0.7])

% [“#1984c5”, "#22a7f0”, “#63bff0”, “#a7d5ed”, “#e2e2e2”, “#e1a692”, “#de6e56”, “#e14b31”, “#c23728”]
plot(slit_curve(1:41,2),LineWidth=1.5,LineStyle=":",Color=[0.1 0.1 0.1])
plot(slit_03(1:41,2),LineWidth=1.5,LineStyle="-",Color="#000080")
plot(slit_05(1:41,2),LineWidth=1.5,LineStyle="--",Color="#004d00")
plot(slit_07(1:41,2),LineWidth=1.5,LineStyle="-",Color="#800020")
plot(slit_09(1:41,2 ),LineWidth=1.5,LineStyle="--",Color="#B8860B")

legend({"Serpenoid", "gamma = 0.3", "gamma = 0.5", "gamma = 0.7", "gamma = 0.9"},'NumColumns',2,FontSize=9,FontName='arial',Location='northeast');

t = 0:5:200;
xticks(t);
xticklabels(t*0.05);
xlim([0 42]);
a = get(gca,'YTickLabel');  
set(gca,'YTickLabel',a,'fontsize',11,'FontWeight','bold')

pos = -pi/2:pi/6:pi/2;
yticks(pos);
yticklabels({"-\pi/2", "-\pi/3", "-\pi/6", "0", "\pi/6", "\pi/3", "\pi/2"});
ylim([-pi/2.99 pi/2]);
a = get(gca,'XTickLabel');  
set(gca,'XTickLabel',a,'fontsize',11,'FontWeight','bold')

grid on;
% 
grid_ax = gca;
grid_ax.LineWidth = 1;
grid_ax.GridLineStyle = "--";
grid_ax.GridColor = [0.2 0.2 0.2];
% grid_ax.YGrid = "off";

xlabel("Time (sec)","FontSize",13,"FontName","arial","FontWeight","bold");
ylabel("Lateral joint position (rad)","FontSize",13,"FontName","arial","FontWeight","bold");

pbaspect([2 1.1 0.8]);

%%
figure;

plot(p_head_log(:,1),p_head_log(:,2))

xlim([-2 2])
ylim([-1 1])

pbaspect([2 1 0.8]);
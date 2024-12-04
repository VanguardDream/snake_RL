clc; clear

%%
load L_ori_map_.mat
smooth_U = movmean(U_result,5);

x_min = min(smooth_U(:,1));
x_max = max(smooth_U(:,1));

y_min = min(smooth_U(:,2));
y_max = max(smooth_U(:,2));

z_min = min(smooth_U(:,3));
z_max = max(smooth_U(:,3));

%%
numInterp = 300;
t = 1:101;
tInterp = linspace(1, 101, numInterp);

xInterp = interp1(t, smooth_U(:,1), tInterp, "spline");
yInterp = interp1(t, smooth_U(:,2), tInterp, "spline");
zInterp = interp1(t, smooth_U(:,3), tInterp, "spline");

%%
C = 1:1:300;

%%
xInterp = (180/pi) * xInterp;
yInterp = (180/pi) * yInterp;
zInterp = (180/pi) * zInterp;

%% XY
figure;
scatter3(xInterp, yInterp, zInterp, 48, C, "filled","o","MarkerEdgeColor",'k','LineWidth',0.1,'MarkerFaceAlpha',0.7);
colormap(pink)

hold on;

xlabel("X axis orientation");
ylabel("Y axis orientation");
zlabel("Z axis orientation");

ax = gca; %let user change axis setting
ax.FontSize = 10; %axis fontsize 
ax.LineWidth = 1.5; ax.FontWeight="bold"; %axis linewidth and Fontweight
ax.GridLineStyle = '-';
ax.GridLineWidth = 1.0;
ax.GridColor=[0.8 0.8 0.8];
ax.Color=[0.3 0.3 0.3];
fontname(gcf,"Arial") 
% pbaspect([1 1 1])
axis equal;

% 축 범위를 설정하여 정육면체 보장
xRange = 1.2 * [min(xInterp), max(xInterp)];
yRange = 1.2 * [min(yInterp), max(yInterp)];
zRange = 1.2 * [min(zInterp), max(zInterp)];
maxRange = max([diff(xRange), diff(yRange), diff(zRange)]); % 최대 범위
centerX = mean(xRange);
centerY = mean(yRange);
centerZ = mean(zRange);

% 동일한 범위 설정
xlim([centerX - maxRange/2, centerX + maxRange/2]);
ylim([centerY - maxRange/2, centerY + maxRange/2]);
zlim([centerZ - maxRange/2, centerZ + maxRange/2]);

xticks(-180:10:180);

% set(gca, 'YDir', 'reverse');

view(180,-90);
box on;

plot3([-360, 360], [0, 0], [0, 0], 'k:', 'LineWidth', 1.75); % X축
plot3([0, 0], [-360, 360], [0, 0], 'k:', 'LineWidth', 1.75); % Y축
plot3([0, 0], [0, 0], [-360, 360], 'k:', 'LineWidth', 1.75); % Z축

hold off;
%% XZ
figure;
scatter3(xInterp, yInterp, zInterp, 36, C, "filled","o","MarkerEdgeColor",'k','LineWidth',0.1,'MarkerFaceAlpha',0.7);
colormap(pink)

hold on;

xlabel("X axis orientation");
ylabel("Y axis orientation");
zlabel("Z axis orientation");

ax = gca; %let user change axis setting
ax.FontSize = 10; %axis fontsize 
ax.LineWidth = 1.5; ax.FontWeight="bold"; %axis linewidth and Fontweight
ax.GridLineStyle = '-';
ax.GridLineWidth = 1.0;
ax.GridColor=[0.8 0.8 0.8];
ax.Color=[0.3 0.3 0.3];
fontname(gcf,"Arial") 
% pbaspect([1 1 1])
axis equal;

% 축 범위를 설정하여 정육면체 보장
xRange = 1.2 * [min(xInterp), max(xInterp)];
yRange = 1.2 * [min(yInterp), max(yInterp)];
zRange = 1.2 * [min(zInterp), max(zInterp)];
maxRange = max([diff(xRange), diff(yRange), diff(zRange)]); % 최대 범위
centerX = mean(xRange);
centerY = mean(yRange);
centerZ = mean(zRange);

% 동일한 범위 설정
xlim([centerX - maxRange/2, centerX + maxRange/2]);
ylim([centerY - maxRange/2, centerY + maxRange/2]);
zlim([centerZ - maxRange/2, centerZ + maxRange/2]);

xticks(-180:10:180);

% set(gca, 'YDir', 'reverse');

view(0,0);
box on;

plot3([-360, 360], [0, 0], [0, 0], 'k:', 'LineWidth', 1.75); % X축
plot3([0, 0], [-360, 360], [0, 0], 'k:', 'LineWidth', 1.75); % Y축
plot3([0, 0], [0, 0], [-360, 360], 'k:', 'LineWidth', 1.75); % Z축

hold off;

%% YZ
figure;
scatter3(xInterp, yInterp, zInterp, 36, C, "filled","o","MarkerEdgeColor",'k','LineWidth',0.1,'MarkerFaceAlpha',0.7);
colormap(pink)

hold on;

xlabel("X axis orientation");
ylabel("Y axis orientation");
zlabel("Z axis orientation");

ax = gca; %let user change axis setting
ax.FontSize = 10; %axis fontsize 
ax.LineWidth = 1.5; ax.FontWeight="bold"; %axis linewidth and Fontweight
ax.GridLineStyle = '-';
ax.GridLineWidth = 1.0;
ax.GridColor=[0.8 0.8 0.8];
ax.Color=[0.3 0.3 0.3];
fontname(gcf,"Arial") 
% pbaspect([1 1 1])
axis equal;

% 축 범위를 설정하여 정육면체 보장
xRange = 1.2 * [min(xInterp), max(xInterp)];
yRange = 1.2 * [min(yInterp), max(yInterp)];
zRange = 1.2 * [min(zInterp), max(zInterp)];
maxRange = max([diff(xRange), diff(yRange), diff(zRange)]); % 최대 범위
centerX = mean(xRange);
centerY = mean(yRange);
centerZ = mean(zRange);

% 동일한 범위 설정
xlim([centerX - maxRange/2, centerX + maxRange/2]);
ylim([centerY - maxRange/2, centerY + maxRange/2]);
zlim([centerZ - maxRange/2, centerZ + maxRange/2]);

view(90,0);
box on;
yticks(-180:10:180);

plot3([-360, 360], [0, 0], [0, 0], 'k:', 'LineWidth', 1.75); % X축
plot3([0, 0], [-360, 360], [0, 0], 'k:', 'LineWidth', 1.75); % Y축
plot3([0, 0], [0, 0], [-360, 360], 'k:', 'LineWidth', 1.75); % Z축

hold off;

%% 등각
figure;
scatter3(xInterp, yInterp, zInterp, 36, C, "filled","o","MarkerEdgeColor",'k','LineWidth',0.1,'MarkerFaceAlpha',0.7);
colormap(pink)

hold on;

xlabel("X axis orientation");
ylabel("Y axis orientation");
zlabel("Z axis orientation");

ax = gca; %let user change axis setting
ax.FontSize = 10; %axis fontsize 
ax.LineWidth = 1.5; ax.FontWeight="bold"; %axis linewidth and Fontweight
ax.GridLineStyle = '-';
ax.GridLineWidth = 1.0;
ax.GridColor=[0.8 0.8 0.8];
ax.Color=[0.3 0.3 0.3];
fontname(gcf,"Arial") 

pbaspect([4 3 1])

cb = colorbar;
% cb.Ticks = linspace(0, 54, 10);
% tmp_tick = round((linspace(0, 54, 10) * (1/27)), 1);
% cb.TickLabels = round((linspace(0, 54, 10) * (1/27)), 1);
% cb.Label.String = "J term weight";
cb.Label.FontSize = 10;
cb.Location = "south";

% 축 범위를 설정하여 정육면체 보장
xRange = 1.2 * [min(xInterp), max(xInterp)];
yRange = 1.2 * [min(yInterp), max(yInterp)];
zRange = 1.2 * [min(zInterp), max(zInterp)];
maxRange = max([diff(xRange), diff(yRange), diff(zRange)]); % 최대 범위
centerX = mean(xRange);
centerY = mean(yRange);
centerZ = mean(zRange);

% 동일한 범위 설정
xlim([centerX - maxRange/2, centerX + maxRange/2]);
ylim([centerY - maxRange/2, centerY + maxRange/2]);
zlim([centerZ - maxRange/2, centerZ + maxRange/2]);

view(0,90);
box on;
xticks(-180:10:180);
yticks(-180:10:180);
zticks(-180:10:180);

plot3([-360, 360], [0, 0], [0, 0], 'k-', 'LineWidth', 1.5); % X축
plot3([0, 0], [-360, 360], [0, 0], 'k-', 'LineWidth', 1.5); % Y축
plot3([0, 0], [0, 0], [-360, 360], 'k-', 'LineWidth', 1.5); % Z축

hold off;
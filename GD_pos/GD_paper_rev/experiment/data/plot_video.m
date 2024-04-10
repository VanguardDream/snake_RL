clc; clear;
%% load
% load roll_data.mat;
% data = videorolldata;

% load side_data.mat;
% load side_cover_data.mat;
% data = videosidedata;

load slit_data.mat;
data = videoslitdata;


clear videorolldata videosidedata videoslitdata
%% 영점 맞추기
zeros = data(1,:);

data = data - zeros;
clear zeros
%% Case별 평균
t = table2array(data(1:301,4));

% curve
i = 1;

x = table2array(data(1:301,3 * i - 1)) + table2array(data(1:301,3 * (i + 1) - 1)) + table2array(data(1:301,3 * (i + 2) - 1));
y = table2array(data(1:301,3 * i)) + table2array(data(1:301,3 * (i + 1))) + table2array(data(1:301,3 * (i + 2)));

x = x/3; y = y/3;

curve = array2table([t x y],"VariableNames",{'t','x','y'});

% gamma 03
i = 4;

x = table2array(data(1:301,3 * i - 1)) + table2array(data(1:301,3 * (i + 1) - 1)) + table2array(data(1:301,3 * (i + 2) - 1));
y = table2array(data(1:301,3 * i)) + table2array(data(1:301,3 * (i + 1))) + table2array(data(1:301,3 * (i + 2)));

x = x/3; y = y/3;

gamma03 = array2table([t x y],"VariableNames",{'t','x','y'});

% gamma 05
i = 7;

x = table2array(data(1:301,3 * i - 1)) + table2array(data(1:301,3 * (i + 1) - 1)) + table2array(data(1:301,3 * (i + 2) - 1));
y = table2array(data(1:301,3 * i)) + table2array(data(1:301,3 * (i + 1))) + table2array(data(1:301,3 * (i + 2)));

x = x/3; y = y/3;

gamma05 = array2table([t x y],"VariableNames",{'t','x','y'});

% gamma 07
i = 10;

x = table2array(data(1:301,3 * i - 1)) + table2array(data(1:301,3 * (i + 1) - 1)) + table2array(data(1:301,3 * (i + 2) - 1));
y = table2array(data(1:301,3 * i)) + table2array(data(1:301,3 * (i + 1))) + table2array(data(1:301,3 * (i + 2)));

x = x/3; y = y/3;

gamma07 = array2table([t x y],"VariableNames",{'t','x','y'});

% gamma 09
i = 13;

x = table2array(data(1:301,3 * i - 1)) + table2array(data(1:301,3 * (i + 1) - 1)) + table2array(data(1:301,3 * (i + 2) - 1));
y = table2array(data(1:301,3 * i)) + table2array(data(1:301,3 * (i + 1))) + table2array(data(1:301,3 * (i + 2)));

x = x/3; y = y/3;

gamma09 = array2table([t x y],"VariableNames",{'t','x','y'});

% clear data i t x y

%% Case 모든 데이터 정리
t = table2array(data(1:301,4));

% curve
i = 1;

x_all = [table2array(data(1:301,3 * i - 1)), table2array(data(1:301,3 * (i + 1) - 1)), table2array(data(1:301,3 * (i + 2) - 1))];
y_all = [table2array(data(1:301,3 * i)), table2array(data(1:301,3 * (i + 1))), table2array(data(1:301,3 * (i + 2)))];

curve_all = array2table([x_all y_all]);

%% gamma 03
i = 4;

x_all = [table2array(data(1:301,3 * i - 1)), table2array(data(1:301,3 * (i + 1) - 1)), table2array(data(1:301,3 * (i + 2) - 1))];
y_all = [table2array(data(1:301,3 * i)), table2array(data(1:301,3 * (i + 1))), table2array(data(1:301,3 * (i + 2)))];

gamma03_all = array2table([x_all y_all]);

% gamma 05
i = 7;

x_all = [table2array(data(1:301,3 * i - 1)), table2array(data(1:301,3 * (i + 1) - 1)), table2array(data(1:301,3 * (i + 2) - 1))];
y_all = [table2array(data(1:301,3 * i)), table2array(data(1:301,3 * (i + 1))), table2array(data(1:301,3 * (i + 2)))];

gamma05_all = array2table([x_all y_all]);

% gamma 07
i = 10;

x_all = [table2array(data(1:301,3 * i - 1)), table2array(data(1:301,3 * (i + 1) - 1)), table2array(data(1:301,3 * (i + 2) - 1))];
y_all = [table2array(data(1:301,3 * i)), table2array(data(1:301,3 * (i + 1))), table2array(data(1:301,3 * (i + 2)))];

gamma07_all = array2table([x_all y_all]);

% gamma 09
i = 13;

x_all = [table2array(data(1:301,3 * i - 1)), table2array(data(1:301,3 * (i + 1) - 1)), table2array(data(1:301,3 * (i + 2) - 1))];
y_all = [table2array(data(1:301,3 * i)), table2array(data(1:301,3 * (i + 1))), table2array(data(1:301,3 * (i + 2)))];

gamma09_all = array2table([x_all y_all]);

clear data i x_all y_all

%% Plot하기 (side)

figure;
hold on;

% plot(curve.y,curve.x)
% plot(gamma03.y,gamma03.x)
% plot(gamma05.y,gamma05.x)
% plot(gamma07.y,gamma07.x)
% plot(gamma09.y,gamma09.x)

p1 = plot(curve.y,curve.x,LineWidth=1.5,LineStyle=":",Color=[0.1 0.1 0.1]); p1.Color(4) = 0.5;
p2 = plot(gamma03.y,gamma03.x,LineWidth=1.5,LineStyle="-",Color="#000080"); p2.Color(4) = 0.5;
p3 = plot(gamma05.y,gamma05.x,LineWidth=1.5,LineStyle="-",Color="#004d00"); p3.Color(4) = 0.5;
p4 = plot(gamma07.y,gamma07.x,LineWidth=1.5,LineStyle="-",Color="#800020"); p4.Color(4) = 0.5;
p5 = plot(gamma09.y,gamma09.x,LineWidth=1.5,LineStyle="-",Color="#B8860B"); p5.Color(4) = 0.5;

% legend({"Serpenoid", "gamma = 0.3", "gamma = 0.5", "gamma = 0.7", "gamma = 0.9"},'NumColumns',3,FontSize=9,FontName='arial',Location='northwest',Fontweight='bold');
legend({"Serpenoid", "gamma = 0.3", "gamma = 0.5", "gamma = 0.7", "gamma = 0.9"},'NumColumns',2,FontSize=9,FontName='arial',Location='northwest',Fontweight='bold');

ax = gca;
X = ax.XAxis;
Y = ax.YAxis;
X.FontSize = 11;
Y.FontSize = 11;
X.FontName = 'arial';
Y.FontName = 'arial';
X.FontWeight = 'bold';
Y.FontWeight = 'bold';

scale = 2.2;
defaultx = [-1 * scale * 2, scale * 2];
defaulty = [-1 * scale, scale];

xlim(defaultx + 3)
ylim(defaulty + 0.5)

grid on;
grid_ax = gca;
grid_ax.LineWidth = 1;
grid_ax.GridLineStyle = "--";
grid_ax.GridColor = [0.2 0.2 0.2];
grid_ax.Color = '#FEF9D7';

pbaspect([2 1 1])

xlabel("x (m)","FontSize",13,"FontName","arial","FontWeight","bold");
ylabel("y (m)","FontSize",13,"FontName","arial","FontWeight","bold");

%% Plot하기 (roll)

figure;
hold on;

% plot(curve.y,curve.x)
% plot(gamma03.y,gamma03.x)
% plot(gamma05.y,gamma05.x)
% plot(gamma07.y,gamma07.x)
% plot(gamma09.y,gamma09.x)

p1 = plot(curve.y,curve.x,LineWidth=1.5,LineStyle=":",Color=[0.1 0.1 0.1]); p1.Color(4) = 0.5;
p2 = plot(gamma03.y,gamma03.x,LineWidth=1.5,LineStyle="-",Color="#000080"); p2.Color(4) = 0.5;
p3 = plot(gamma05.y,gamma05.x,LineWidth=1.5,LineStyle="-",Color="#004d00"); p3.Color(4) = 0.5;
p4 = plot(gamma07.y,gamma07.x,LineWidth=1.5,LineStyle="-",Color="#800020"); p4.Color(4) = 0.5;
p5 = plot(gamma09.y,gamma09.x,LineWidth=1.5,LineStyle="-",Color="#B8860B"); p5.Color(4) = 0.5;

legend({"Serpenoid", "gamma = 0.3", "gamma = 0.5", "gamma = 0.7", "gamma = 0.9"},'NumColumns',1,FontSize=9,FontName='arial',Location='southwest',Fontweight='bold');
% legend({"Serpenoid", "gamma = 0.3", "gamma = 0.5", "gamma = 0.7", "gamma = 0.9"},'NumColumns',2,FontSize=9,FontName='arial',Location='northwest',Fontweight='bold');

ax = gca;
X = ax.XAxis;
Y = ax.YAxis;
X.FontSize = 11;
Y.FontSize = 11;
X.FontName = 'arial';
Y.FontName = 'arial';
X.FontWeight = 'bold';
Y.FontWeight = 'bold';

scale = 1.2;
defaultx = [-1 * scale * 2, scale * 2];
defaulty = [-1 * scale, scale];

xlim(defaultx + 1.5)
ylim(defaulty - 1)

grid on;
grid_ax = gca;
grid_ax.LineWidth = 1;
grid_ax.GridLineStyle = "--";
grid_ax.GridColor = [0.2 0.2 0.2];
grid_ax.Color = '#FEF9D7';

pbaspect([2 1 1])

xlabel("x (m)","FontSize",13,"FontName","arial","FontWeight","bold");
ylabel("y (m)","FontSize",13,"FontName","arial","FontWeight","bold");

%% Plot하기 (slit)

figure;
hold on;

% plot(curve.y,curve.x)
% plot(gamma03.y,gamma03.x)
% plot(gamma05.y,gamma05.x)
% plot(gamma07.y,gamma07.x)
% plot(gamma09.y,gamma09.x)

p1 = plot(curve.x,-curve.y,LineWidth=1.5,LineStyle=":",Color=[0.1 0.1 0.1]); p1.Color(4) = 0.5;
p2 = plot(gamma03.x,-gamma03.y,LineWidth=1.5,LineStyle="-",Color="#000080"); p2.Color(4) = 0.5;
p3 = plot(gamma05.x,-gamma05.y,LineWidth=1.5,LineStyle="-",Color="#004d00"); p3.Color(4) = 0.5;
p4 = plot(gamma07.x,-gamma07.y,LineWidth=1.5,LineStyle="-",Color="#800020"); p4.Color(4) = 0.5;
p5 = plot(gamma09.x,-gamma09.y,LineWidth=1.5,LineStyle="-",Color="#B8860B"); p5.Color(4) = 0.5;

legend({"Serpenoid", "gamma = 0.3", "gamma = 0.5", "gamma = 0.7", "gamma = 0.9"},'NumColumns',1,FontSize=9,FontName='arial',Location='northeast',Fontweight='bold');
% legend({"Serpenoid", "gamma = 0.3", "gamma = 0.5", "gamma = 0.7", "gamma = 0.9"},'NumColumns',2,FontSize=9,FontName='arial',Location='northwest',Fontweight='bold');

ax = gca;
X = ax.XAxis;
Y = ax.YAxis;
X.FontSize = 11;
Y.FontSize = 11;
X.FontName = 'arial';
Y.FontName = 'arial';
X.FontWeight = 'bold';
Y.FontWeight = 'bold';

scale = 0.70;
defaultx = [-1 * scale * 2, scale * 2];
defaulty = [-1 * scale, scale];

y_tick = -5:0.5:5;
yticks(y_tick);

xlim(defaultx + 0.75)
ylim(defaulty - 0.05)

grid on;
grid_ax = gca;
grid_ax.LineWidth = 1;
grid_ax.GridLineStyle = "--";
grid_ax.GridColor = [0.2 0.2 0.2];
grid_ax.Color = '#FEF9D7';

pbaspect([2 1 1])

xlabel("x (m)","FontSize",13,"FontName","arial","FontWeight","bold");
ylabel("y (m)","FontSize",13,"FontName","arial","FontWeight","bold");

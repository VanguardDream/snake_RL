clc; clear;
%% load
% load roll_data.mat;
% data = videorolldata;

load side_data.mat;
load side_cover_data.mat;
data = videosidedata;

% load slit_data.mat;
% data = videoslitdata;


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

clear data i t x y
%% Plot하기 (side)

figure;
hold on;

plot(curve.y,curve.x)
plot(sidecoverdata.y,sidecoverdata.x)
% plot(gamma03.x,gamma03.y)
% plot(gamma05.x,gamma05.y)
% plot(gamma07.x,gamma07.y)
% plot(gamma09.x,gamma09.y)

ax = gca;
X = ax.XAxis;
Y = ax.YAxis;
X.FontSize = 11;
Y.FontSize = 11;
X.FontName = 'arial';
Y.FontName = 'arial';
X.FontWeight = 'bold';
Y.FontWeight = 'bold';

scale = 2.1;
defaultx = [-1 * scale * 2, scale * 2];
defaulty = [-1 * scale, scale];

xlim(defaultx + 3)
ylim(defaulty)

% axis off

pbaspect([2 1 1])
set(gca,'Color','none')
exportgraphics(ax,'t.png')

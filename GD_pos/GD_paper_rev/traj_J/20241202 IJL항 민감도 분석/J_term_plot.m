clc; clear;
%%
load J_maps_ordered.mat

%% 안씀
% total_map = [
%     map1(101,:,:);
%     map1(94,:,:);
%     map1(93,:,:);
%     map1(87,:,:);
%     map1(86,:,:);
%     map1(85,:,:);
%     map1(84,:,:);
%     map1(80,:,:);
%     map1(78,:,:);
%     map1(75,:,:);
%     map1(73,:,:);
%     map1(70,:,:);
%     map1(64,:,:);
%     map1(61,:,:);
%     map1(57,:,:);
%     map1(50,:,:);
%     map1(49,:,:);
%     map1(47,:,:);
%     map1(43,:,:);
%     map1(41,:,:);
%     map1(40,:,:);
%     map1(36,:,:);
%     map1(35,:,:);
%     map1(34,:,:);
%     map1(33,:,:);
%     map1(32,:,:);
%     map1(31,:,:);
%     map1(29,:,:);
%     map1(28,:,:);
%     map1(27,:,:);
%     map1( 9,:,:);
%     map1( 7,:,:);
%     map1( 6,:,:);
%     map1( 5,:,:);
%     map1( 4,:,:);
%     map1( 3,:,:);
%     map1( 2,:,:);
%     map1( 1,:,:);
%     map2(78,:,:); %2 시작
%     map2(68,:,:);
%     map2(62,:,:);
%     map2(59,:,:);
%     map2(47,:,:);
%     map2(96,:,:);
%     map2(95,:,:);
%     map2(94,:,:);
%     map2(93,:,:);
%     map2(92,:,:);
%     map2(91,:,:);
%     map2(73,:,:);
%     map2(72,:,:);
%     map2(67,:,:);
%     map2(56,:,:);
%     map2( 2,:,:);
% ];

% %%
% canvas2 = zeros(500,500);
% num_datasets = 54;
% data_idx = 1:num_datasets;
% 
% for i = data_idx
%     canvas2 = canvas2 + squeeze(total_map(i,:,:));
% end
%%
canvas = zeros(500,500);
num_datasets = 54;
data_idx = 1:num_datasets;
for i=data_idx
    for x=1:size(squeeze(total_map(i,:,:)),1)
        for y=1:size(squeeze(total_map(i,:,:)),2)

            if total_map(i,x,y) ~= 0
                canvas(x,y) = i;
            end
        end
    end
end

%%
x_ticks = 1:1:500;
x_ticks = (x_ticks - 250) / 300;


canvas_t = transpose(canvas);

figure;
s = pcolor(canvas_t);
s.EdgeColor = 'none';

colormap("pink");
cb = colorbar;
cb.Ticks = linspace(0, 54, 10);
tmp_tick = round((linspace(0, 54, 10) * (1/27)), 1);
cb.TickLabels = round((linspace(0, 54, 10) * (1/27)), 1);
cb.Label.String = "J term weight";
cb.Label.FontSize = 10;
% cb.AxisLocation ="in";
% cb.Location = "west";
% cb.Color = [0.8 0.8 0.8];

xlabel("X (m)","FontSize",13,"FontName","arial","FontWeight","bold");
ylabel("Y (m)","FontSize",13,"FontName","arial","FontWeight","bold");

xlim([200 500]);
ylim([(220 - 125) (220 + 125)]);

ttick = [1 50:50:500];
ttick_label = linspace(-1.5,1.5,11);
ttick_label = round(ttick_label,2);

xticks(ttick);
yticks(ttick);
xticklabels(ttick_label);
yticklabels(ttick_label);

hold on;

x1 = xline(200, LineWidth=0.75, LineStyle="--", Color=[0.8 0.8 0.8]);
x2 = xline(250, LineWidth=1.5, LineStyle="-", Color=[0.8 0.8 0.8]);
x3 = xline(300, LineWidth=0.75, LineStyle="--", Color=[0.8 0.8 0.8]);
x4 = xline(350, LineWidth=0.75, LineStyle="--", Color=[0.8 0.8 0.8]);
x5 = xline(400, LineWidth=0.75, LineStyle="--", Color=[0.8 0.8 0.8]);
x6 = xline(450, LineWidth=0.75, LineStyle="--", Color=[0.8 0.8 0.8]);

x1.Alpha = 0.3;
x2.Alpha = 0.5;
x3.Alpha = 0.3;
x4.Alpha = 0.3;
x5.Alpha = 0.3;
x6.Alpha = 0.3;

y1 = yline(100, LineWidth=0.75, LineStyle="--", Color=[0.8 0.8 0.8]);
y2 = yline(150, LineWidth=0.75, LineStyle="--", Color=[0.8 0.8 0.8]);
y3 = yline(200, LineWidth=0.75, LineStyle="--", Color=[0.8 0.8 0.8]);
y4 = yline(250, LineWidth=1.5, LineStyle="-", Color=[0.8 0.8 0.8]);
y5 = yline(300, LineWidth=0.75, LineStyle="--", Color=[0.8 0.8 0.8]);
y6 = yline(350, LineWidth=0.75, LineStyle="--", Color=[0.8 0.8 0.8]);

y1.Alpha = 0.3;
y2.Alpha = 0.3;
y3.Alpha = 0.3;
y4.Alpha = 0.5;
y5.Alpha = 0.3;
y6.Alpha = 0.3;

ax = gca; %let user change axis setting
ax.FontSize = 10; %axis fontsize 
ax.LineWidth = 1.5; ax.FontWeight="bold"; %axis linewidth and Fontweight
ax.GridLineStyle = ':';
ax.GridLineWidth = 1.5;
ax.GridColor='#101010';
ax.Color=[0.85 0.85 0.85];
fontname(gcf,"Arial") 
pbaspect([300 250 1])

%%
for i = data_idx
    figure;
    s = pcolor(squeeze(total_map(i,:,:)));
    s.EdgeColor = 'none';
end
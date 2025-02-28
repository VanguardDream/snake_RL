clc; clear;
%%
load("sim_data.mat")
t = 0.1:0.1:length(x_vel)/10;
%%
h=figure('Units', 'centimeters', 'Position', [5, 5, 15, 10]);

ax = gca; %let user change axis setting
ax.FontSize = 11; %axis fontsize 
ax.LineWidth = 1.0; ax.FontWeight="bold"; %axis linewidth and Fontweight
ax.GridColor='#202020';
fontname(gcf,"Arial") 
ax.Color=[0.95 0.95 0.95];
box
pbaspect([2.1 1 1])

hold on;

yyaxis left

plot(t, x_vel, 'Color', 'r', 'LineStyle', '-', 'LineWidth', 1.5, 'DisplayName', 'X vel.'); 
plot(t, y_vel, 'Color', 'b', 'LineStyle', '-', 'LineWidth', 1.5, 'DisplayName', 'Y vel.'); 
ylabel('m/s');
ylim([-1.1 2.2]);

yyaxis right
plot(t, yaw_vel, 'Color', 'g', 'LineStyle', '-', 'LineWidth', 1.5, 'DisplayName', 'Yaw vel.'); 

xlabel('Time (sec.)');
ylabel('rad/s');
ylim([-1.1 2.2]);

legend(Location='northeast',NumColumns=3);
hold off;

ax = gca;
ax.YAxis(1).Color = 'k';
ax.YAxis(2).Color = [0 0.5 0.1];

grid on;
box on;
grid minor;


%%
vel_vec = [x_vel' y_vel' yaw_vel'];

mean_vel_vec = movmean(vel_vec,[19 0]);
%%
h=figure('Units', 'centimeters', 'Position', [5, 5, 15, 10]);

ax = gca; %let user change axis setting
ax.FontSize = 11; %axis fontsize 
ax.LineWidth = 1.0; ax.FontWeight="bold"; %axis linewidth and Fontweight
ax.GridColor='#202020';
fontname(gcf,"Arial") 
ax.Color=[0.95 0.95 0.95];
box
pbaspect([2.1 1 1])

hold on;

yyaxis left

plot(t, mean_vel_vec(:,1), 'Color', 'r', 'LineStyle', '-', 'LineWidth', 1.5, 'DisplayName', 'X vel.'); 
plot(t, mean_vel_vec(:,2), 'Color', 'b', 'LineStyle', '-', 'LineWidth', 1.5, 'DisplayName', 'Y vel.'); 
ylabel('m/s');
ylim([-1.1 2.2]);

yyaxis right
plot(t, mean_vel_vec(:,3), 'Color', 'g', 'LineStyle', '-', 'LineWidth', 1.5, 'DisplayName', 'Yaw vel.'); 

xlabel('Time (sec.)');
ylabel('rad/s');
ylim([-1.1 2.2]);

legend(Location='northeast',NumColumns=3);
hold off;

ax = gca;
ax.YAxis(1).Color = 'k';
ax.YAxis(2).Color = [0 0.5 0.1];

grid on;
box on;
grid minor;

%%
scale_k = 0.7; % 실제 뱀로봇 속도와 조이스틱 범위 스케일링을 위한 계수
beta = 1; % 크기 차이에 대한 민감도를 조절하는 계수
scale_r = 2.1; % 회전에 대한 스케일을 조절하는 계수
alpha = 1; % 회전에 대한 민감도를 조절하는 계수
forward_reward_weight = 6.5;

joy_vec = [0.5 0.5 0];

for i = 1:1:length(mean_vel_vec)
    if norm(joy_vec) < 1e-1
        for_rew_mean(i) = forward_reward_weight * (1 / (1 + norm(mean_vel_vec(i,:))));
        for_rew(i) = forward_reward_weight * (1 / (1 + norm(vel_vec(i,:))));
    else
        for_rew_mean(i) = forward_reward_weight * dot(mean_vel_vec(i,:), joy_vec) / (norm(mean_vel_vec(i,:)) * norm(joy_vec) + 1e-6);
        for_rew(i) = forward_reward_weight * dot(vel_vec(i,:), joy_vec) / (norm(vel_vec(i,:)) * norm(joy_vec) + 1e-6);
    end
    % magnitude_rew = forward_reward_weight * exp(-beta * abs(norm(vel_vec(i,:)) - scale_k * norm(joy_vec)));
    % magnitude_rew_mean = forward_reward_weight * exp(-beta * abs(norm(mean_vel_vec(i,:)) - scale_k * norm(joy_vec)));

    % for_rew(i) = for_rew(i) + magnitude_rew;
    % for_rew_mean(i) = for_rew_mean(i) + magnitude_rew_mean;

end

%%
h=figure('Units', 'centimeters', 'Position', [5, 5, 15, 10]);

ax = gca; %let user change axis setting
ax.FontSize = 11; %axis fontsize 
ax.LineWidth = 1.0; ax.FontWeight="bold"; %axis linewidth and Fontweight
ax.GridColor='#202020';
fontname(gcf,"Arial") 
ax.Color=[0.95 0.95 0.95];
box
pbaspect([2.1 1 1])

hold on;

xlabel('Time Step');

plot(for_rew, 'Color', 'b', 'LineStyle', '-', 'LineWidth', 1.5, 'DisplayName', 'Raw Value'); 
plot(for_rew_mean, 'Color', 'r', 'LineStyle', '-', 'LineWidth', 1.5, 'DisplayName', 'Mean Value'); 

ylabel('Reward');


yline(mean(for_rew_mean), 'LineStyle', '-', 'LineWidth', 1.5, 'DisplayName', 'Avg. Mean Value')
yline(mean(for_rew), 'LineStyle', ':', 'LineWidth', 1.5, 'DisplayName', 'Mean Value')

legend(Location='northeast',NumColumns=2);
hold off;

ax = gca;

grid on;
box on;
grid minor;

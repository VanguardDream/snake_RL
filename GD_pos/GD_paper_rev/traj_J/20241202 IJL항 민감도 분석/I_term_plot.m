clc; clear;
%%
load I_plot_data.mat


smooth_I = movmean(I_term,3);
smooth_J = movmean(J_term,3);
smooth_L = movmean(L_term,3);

U_origin = 1.5 * smooth_I + 1.0 * smooth_J - 0.2 * smooth_L;

%%
figure;

x_ticks = 0:0.1:10;

yyaxis left
plot(x_ticks,smooth_I * 10, LineWidth=1.2);
ylabel("Velocity ( cm/s )","FontSize",13,"FontName","arial","FontWeight","bold");

yyaxis right
plot(x_ticks, U_origin, LineWidth=1.2);
ylabel("Utility Function Value","FontSize",13,"FontName","arial","FontWeight","bold");

grid on;
box on;
grid_ax = gca;
grid_ax.LineWidth = 1;
grid_ax.GridLineStyle = "--";
grid_ax.GridColor = [0.2 0.2 0.2];
% grid_ax.Color = '#FEF9D7';

xlabel("I term weight","FontSize",13,"FontName","arial","FontWeight","bold");
xticks(0:1:10);

xline(1.5,LineWidth=1.2,LineStyle="--",Color='r')

% ylim([3 5.5]);
pbaspect([2 1 1])
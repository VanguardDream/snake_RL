clc; clear;
%%
gait_name = ["Slithering" "Sidewinding" "Rolling"];

gamma_data = [0.6207 0.4721 0.3417 0.2745;
              0.6347 0.5196 0.4519 0.3506;
              0.8751 0.7017 0.6847 0.6701];

legends = ["gamma = 0.3" "gamma = 0.5" "gamma = 0.7" "gamma = 0.9"];

%%
figure;

b = bar(gamma_data);

b(1).FaceColor = [0.1 0.1 0.1];
b(2).FaceColor = [0.3 0.3 0.3];
b(3).FaceColor = [0.5 0.5 0.5];
b(4).FaceColor = [0.7 0.7 0.7];

yticks(0:0.2:1);
yticklabels(["0","0.2","0.4","0.6","0.8","1.0"]);

a = get(gca,'YTickLabel');  
set(gca,'YTickLabel',a,'fontsize',11,'FontWeight','bold')

xticklabels(gait_name);
a = get(gca,'XTickLabel');  
set(gca,'XTickLabel',a,'fontsize',11,'FontWeight','bold')

legend({"gamma = 0.3" "gamma = 0.5" "gamma = 0.7" "gamma = 0.9"},FontSize=9,FontName='arial',Location='northwest');

grid on;
% 
grid_ax = gca;
grid_ax.LineWidth = 1;
grid_ax.GridLineStyle = "--";
grid_ax.GridColor = [0.2 0.2 0.2];
grid_ax.XGrid = "off";

% xlabel("Gait types","FontSize",13,"FontName","arial","FontWeight","bold");
ylabel("Correlation coefficient","FontSize",13,"FontName","arial","FontWeight","bold");

pbaspect([2 1.1 0.8]);

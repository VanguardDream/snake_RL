clc; clear;
%%
gait_name = ["Slithering" "Sidewinding" "Rolling"];

gamma_data = [0.8921 0.7700 0.6760 0.5808;
              0.8823 0.6818 0.4543 0.3604;
              0.9728 0.9196 0.8169 0.7174];

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

legend({"gamma = 0.3" "gamma = 0.5" "gamma = 0.7" "gamma = 0.9"},FontSize=9,FontName='arial',Location='southeast');

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

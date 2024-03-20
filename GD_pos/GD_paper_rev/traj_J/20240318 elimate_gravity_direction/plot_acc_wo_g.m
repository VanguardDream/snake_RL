acc_wo_x = head_acc_wo_g(:,:,1);
dist = U_map(:,:,1);
x_dist = cos(Tf_orientation) .* dist;
rot = sqrt(Rot_vec(:,:,1).^2 + Rot_vec(:,:,2).^2 + Rot_vec(:,:,3).^2);

data = 1.0 * acc_wo_x + 1.5 * x_dist - 0.2 * rot;

figure; hAxes = gca;
contourf(transpose(data),15);

colormap jet;
colorbar;

yticks(0:30:181);
yticklabels(["0","30","60","90","120","150","180"]);
a = get(gca,'YTickLabel');  
set(gca,'YTickLabel',a,'fontsize',11,'FontWeight','bold')

xticks(1:30:181);
xticklabels(["0","30","60","90","120","150","180"]);
a = get(gca,'XTickLabel');  
set(gca,'XTickLabel',a,'fontsize',11,'FontWeight','bold')

xline(31,LineWidth=1,LineStyle="--",Color=[0.8 0.8 0.8]);
xline(61,LineWidth=1,LineStyle="--",Color=[0.8 0.8 0.8]);
xline(91,LineWidth=1,LineStyle="--",Color=[0.8 0.8 0.8]);
xline(121,LineWidth=1,LineStyle="--",Color=[0.8 0.8 0.8]);
xline(151,LineWidth=1,LineStyle="--",Color=[0.8 0.8 0.8]);

yline(30,LineWidth=1,LineStyle="--",Color=[0.8 0.8 0.8]);
yline(60,LineWidth=1,LineStyle="--",Color=[0.8 0.8 0.8]);
yline(90,LineWidth=1,LineStyle="--",Color=[0.8 0.8 0.8]);

xlabel("Spatial parameter (degree)","FontSize",13,"FontName","arial","FontWeight","bold");
ylabel("Temporal parameter (rad)","FontSize",13,"FontName","arial","FontWeight","bold");

pbaspect([6 4 0.8]);

%% Y축

figure

acc_wo_y = head_acc_wo_g(:,:,2);
dist = U_map(:,:,1);
y_dist = abs(sin(Tf_orientation) .* dist);
rot = sqrt(Rot_vec(:,:,1).^2 + Rot_vec(:,:,2).^2 + Rot_vec(:,:,3).^2);

data = 1.0 * acc_wo_y + 1.5 * y_dist - 0.2 * rot;

contourf(transpose(data),15)
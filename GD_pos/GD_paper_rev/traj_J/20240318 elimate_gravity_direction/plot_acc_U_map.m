figure

acc_wo_x = head_acc_wo_g(:,:,1);
dist = U_map(:,:,1);
x_dist = cos(Tf_orientation) .* dist;
rot = sqrt(Rot_vec(:,:,1).^2 + Rot_vec(:,:,2).^2 + Rot_vec(:,:,3).^2);

data = 1.0 * acc_wo_x + 1.5 * x_dist - 0.2 * rot;

contourf(transpose(data),15)

%% Y축

figure

acc_wo_y = head_acc_wo_g(:,:,2);
dist = U_map(:,:,1);
y_dist = abs(sin(Tf_orientation) .* dist);
rot = sqrt(Rot_vec(:,:,1).^2 + Rot_vec(:,:,2).^2 + Rot_vec(:,:,3).^2);

data = 1.0 * acc_wo_y + 1.5 * y_dist - 0.2 * rot;

contourf(transpose(data),15)
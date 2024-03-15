figure

acc = sqrt(head_acc(:,:,1).^2+head_acc(:,:,2).^2+head_acc(:,:,3).^2) + 1;
dist = U_map(:,:,1);
rot = sqrt(Rot_vec(:,:,1).^2 + Rot_vec(:,:,2).^2 + Rot_vec(:,:,3).^2);


% data = dist ./ acc - rot;
data = dist + acc - rot;
% 
% data = min(data, 40);
% data = max(data, -40);

contourf(transpose(data))
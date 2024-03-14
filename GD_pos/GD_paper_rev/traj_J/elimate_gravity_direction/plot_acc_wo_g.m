figure

acc = head_acc(:,:,1) ./ (abs(head_acc(:,:,3))+0.5) * 5;

acc = min(acc, 400);
acc = max(acc, -800);

dist = U_map(:,:,1);

data = 5 * dist ./ acc;

data = min(data, 40);
data = max(data, -40);

contourf(transpose(data))
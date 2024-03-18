% idx = 13;

data = [];
t_quat = qpos_log(:,4:7);

for idx = 1:1:2000  
    test_quat = t_quat(idx,:);
    
    plane_rotm = quat2rotm([1 0 0 0]);
    test_rotm = quat2rotm(test_quat);
    
    rotm_Origin2This = test_rotm * inv(plane_rotm);
    
    rotated_g = [0 0 9.81] * test_rotm;
    rotated_g = transpose(rotated_g);
    % acc_test = rotm_Origin2This * head_acc_log(idx,:)' 
    
    g_elimated_acc = head_acc_log(idx,:)' - rotated_g;
    % head_acc_log(idx,:)'
    
    % express_acc_in_origin_frame = transpose(g_elimated_acc) * transpose(test_rotm);
    express_acc_in_origin_frame = transpose(g_elimated_acc) * transpose(rotm_Origin2This);
    express_acc_in_origin_frame = transpose(express_acc_in_origin_frame);

    data = [data express_acc_in_origin_frame];
end

data = data';

%%
figure
stackedplot(data);

figure
stackedplot(head_acc_log);

%%
figure
stackedplot(lowpass(data,10,200));

figure
stackedplot(lowpass(head_acc_log,10,200));

%%
mean(data)
mean(head_acc_log)
mean(head_acc_only_log)
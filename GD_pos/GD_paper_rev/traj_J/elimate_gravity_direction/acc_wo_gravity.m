% idx = 13;

data = [];
for idx = 1:1:2000

    t_quat = qpos_log(:,4:7);
    
    test_quat = t_quat(idx,:);
    
    plane_rotm = quat2rotm([1 0 0 0]);
    test_rotm = quat2rotm(test_quat);
    
    rotm_Origin2This = test_rotm * inv(plane_rotm);
    
    rotated_g = plane_rotm * [0; 0; 9.81];
    % acc_test = rotm_Origin2This * head_acc_log(idx,:)' 
    
    g_elimated_acc = head_acc_log(idx,:)' - rotated_g;
    % head_acc_log(idx,:)'
    
    express_acc_in_origin_frame = inv(rotm_Origin2This) * g_elimated_acc;

    data = [data express_acc_in_origin_frame];
end

data = data';

%%
figure
stackedplot(data);

figure
stackedplot(head_acc_log);

mean(data)
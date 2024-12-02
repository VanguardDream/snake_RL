clc; clear;
%%
load Slit_c.mat
% load Serp_c.mat
% load Side_c.mat
% load Roll_c.mat
c_acc = head_acc_wo_g;
c_dist = U_map(:,:,1);
c_rot = sqrt(Rot_vec(:,:,1).^2 + Rot_vec(:,:,2).^2 + Rot_vec(:,:,3).^2);
c_tf = Tf_orientation;

if Motion_lambda(7) > 38
    c_side = true;
else
    c_side = false;
end

clear Curve Gamma head_acc head_acc_wo_g Motion_lambda Rot_vec Tf_orientation U_map

load Slit_0.3.mat
% load Serp_0.9.mat
% load Side_0.3.mat
% load Roll_0.9.mat

% load new_side_0.7.mat
% load newnew_side_0.7.mat
m_acc = head_acc_wo_g;
m_dist = U_map(:,:,1);
m_rot = sqrt(Rot_vec(:,:,1).^2 + Rot_vec(:,:,2).^2 + Rot_vec(:,:,3).^2);
m_tf = Tf_orientation;

if Motion_lambda(7) > 38
    m_side = true;
else
    m_side = false;
end

clear Curve Gamma head_acc head_acc_wo_g Motion_lambda Rot_vec Tf_orientation U_map

%% acc U map

figure;

if c_side
    c_forward_dist = (sin(c_tf) .* c_dist);
    c_forward_acc = c_acc(:,:,2);
    % c_forward_acc = 0;
else
    c_forward_dist = cos(c_tf) .* c_dist;
    c_forward_acc = c_acc(:,:,1);
end

c_data = 1.0 * c_forward_acc + 1.5 * c_forward_dist - 0.2 * c_rot;

c_data = transpose(c_data);

contourf(c_data);

%%
figure;

if m_side
    m_forward_dist = (sin(m_tf) .* m_dist);
    m_forward_acc = m_acc(:,:,2);
    % m_forward_acc = 0;
else
    m_forward_dist = cos(m_tf) .* m_dist;
    m_forward_acc = m_acc(:,:,1);
end

m_data = 1.0 * m_forward_acc + 1.5 * m_forward_dist - 0.2 * m_rot;

m_data = transpose(m_data);

contourf(m_data);

%% 상관계수
% U 값의 상관계수
fprintf("%s","U 상관계수")
norm_U_mat = normalize(m_data);
norm_U_curve = normalize(c_data);

% corr2(norm_U_mat, norm_U_curve)
corr2(m_data,c_data)








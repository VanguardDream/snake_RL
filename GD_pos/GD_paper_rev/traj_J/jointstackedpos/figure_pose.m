%%
joint_pos = rad2deg(qpos_log(end,8:end))

quat = qpos_log(end,4:7);
angles = rad2deg(rotmat2vec3d(quat2rotm(quat)))


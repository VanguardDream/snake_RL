clc; clear;

%%
twoJointRobot = twoJointRigidBodyTree("column");

%%
fx = 2; 
fy = 2;
fz = 0;
nx = 0;
ny = 0;
nz = 3;
eeForce = [nx;ny;nz;fx;fy;fz];
eeName = "tool";

%%
q = [pi/3;pi/4];
Tee = getTransform(twoJointRobot,q,eeName);

show(twoJointRobot, homeConfiguration(twoJointRobot));

hold all;
show(twoJointRobot, q);

%%
J = geometricJacobian(twoJointRobot,q,eeName);
jointTorques = J' * eeForce;
fprintf("Joint torques using geometric Jacobian (Nm): [%.3g, %.3g]",jointTorques);

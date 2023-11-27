clear;
clc;

head = rigidBody('head');
joint1 = rigidBodyJoint('joint1', 'revolute');
joint1.PositionLimits = [-1.5, 1.5];
joint1.JointAxis = [0 1 0];
% tf1 = eul2tform([0 0 -pi/2]) * trvec2tform([-0.2 0 0]); %tf1 translation (xyz)
tf1 = trvec2tform([-0.2 0 0]); %tf1 translation (xyz)
setFixedTransform(joint1,tf1);

head.Joint = joint1;

robot = rigidBodyTree;

addBody(robot,head,'base');

link1 = rigidBody('link1');
joint2 = rigidBodyJoint('joint2', 'revolute');
joint2.PositionLimits = [-1.5, 1.5];
joint2.JointAxis = [0 0 1];
% tf2 = trvec2tform([-0.5 0 0 ]) * eul2tform([0 0 pi/2]);
tf2 = trvec2tform([-0.5 0 0 ]);
setFixedTransform(joint2, tf2)

link1.Joint = joint2;

addBody(robot,link1,'head');

show(robot)
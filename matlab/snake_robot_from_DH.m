clc;clear;

%% DH 로드
load DH.mat;

robot = rigidBodyTree;

%% 링크 구성

bodies = cell(14,1);
joints = cell(14,1);
for i = 1:14
    bodies{i} = rigidBody(['body' num2str(i)]);
    joints{i} = rigidBodyJoint(['jnt' num2str(i)],"revolute");
    setFixedTransform(joints{i},DH(i,:),"dh");
    bodies{i}.Joint = joints{i};
    if i == 1 % Add first body to base
        addBody(robot,bodies{i},"base")
    else % Add current body to previous body by name
        addBody(robot,bodies{i},bodies{i-1}.Name)
    end
end
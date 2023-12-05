clc;clear;

%% DH 로드
load DH.mat;

robot = rigidBodyTree;

%% 링크 구성

bodies = cell(15,1);
joints = cell(15,1);
for i = 1:15
    bodies{i} = rigidBody(['body' num2str(i)]);
    joints{i} = rigidBodyJoint(['jnt' num2str(i)],"revolute");
    setFixedTransform(joints{i},DH(i,:),"mdh");
    joints{i}
    bodies{i}.Joint = joints{i};
    if i == 1 % Add first body to base
        addBody(robot,bodies{i},"base")
    else % Add current body to previous body by name
        addBody(robot,bodies{i},bodies{i-1}.Name)
    end
end

%% 로봇 구성 플롯

show(robot)
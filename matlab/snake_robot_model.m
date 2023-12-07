clear;
clc;

%% Robot 구성 시작
robot = rigidBodyTree;
robot.BaseName = 'base_link';
robot.DataFormat = 'row';
robot.Gravity = [0 0 0];

%% Head 링크 구성 정보
tf_zero = trvec2tform([0 0 0]); %tf1 translation (xyz)

head = rigidBody('head');
head.Mass = 0.116;
head.CenterOfMass = ([-0.019664 0 0]);
head.Inertia = ([36.629 85.359 85.701 0 0 0.899]);
% addVisual(head,"Mesh","C:\Users\Bong\project\snake_RL\matlab\meshes\head.stl", eul2tform([0 0 pi]));
addVisual(head,"Mesh","meshes\head.stl", eul2tform([0 0 pi]));
addCollision(head,"Mesh","meshes\head.stl", eul2tform([0 0 pi]));

base_link_joint = rigidBodyJoint('base_link_joint','fixed');

setFixedTransform(base_link_joint,tf_zero);

head.Joint = base_link_joint;

addBody(robot,head,"base_link");
%% link1 링크 구성 정보
tf_head_joint1 = trvec2tform([-0.035250 0 0 ]);

link1 = rigidBody('link1');
link1.Mass = 0.124;
link1.CenterOfMass = ([-0.050765 0 0]);
link1.Inertia = ([39.160 370.114 371.016 0 2.069 0]);
addVisual(link1,"Mesh","meshes\LinkA.stl");
addCollision(link1,"Mesh","meshes\LinkA.stl");

joint1 = rigidBodyJoint('joint1', 'revolute');
joint1.PositionLimits = [-1.5, 1.5];
joint1.JointAxis = [0 1 0];

setFixedTransform(joint1, tf_head_joint1);

link1.Joint = joint1;

addBody(robot,link1,'head');

%% link2 링크 구성 정보
tf_normal_dis = trvec2tform([-0.0685 0 0 ]);

link2 = rigidBody('link2');
link2.Mass = 0.124;
link2.CenterOfMass = ([-0.050848 0 0]);
link2.Inertia = ([39.160 371.816 370.915 0 0 2.069]);
addVisual(link2,"Mesh","meshes\LinkB.stl");
addCollision(link2,"Mesh","meshes\LinkB.stl");

joint2 = rigidBodyJoint('joint2', 'revolute');
joint2.PositionLimits = [-1.5, 1.5];
joint2.JointAxis = [0 0 1];

setFixedTransform(joint2, tf_normal_dis);

link2.Joint = joint2;

addBody(robot,link2,'link1');
%% 추가 자동 구성
for i=0:1:10
    if mod(i,2) == 0
        refBody = getBody(robot,"link1");

        tmpBody = copy(refBody);

        linkNumber = 3 + i;
        linkName = 'link' + string(linkNumber);

        tmpBody.Name = linkName;
        tmpBody.Joint.Name = 'joint' + string(linkNumber);

        setFixedTransform(tmpBody.Joint, tf_normal_dis);

        addBody(robot,tmpBody, 'link' + string(linkNumber - 1));
     
    else    
        refBody = getBody(robot,"link2");

        tmpBody = copy(refBody);

        linkNumber = 3 + i;
        linkName = 'link' + string(linkNumber);

        tmpBody.Name = linkName;
        tmpBody.Joint.Name = 'joint' + string(linkNumber);

        addBody(robot,tmpBody, 'link' + string(linkNumber - 1));
    end

end

%% Tail 링크 구성 정보
tf_normal_dis = trvec2tform([-0.0685 0 0 ]);

tail = rigidBody('tail');
tail.Mass = 0.051;
tail.CenterOfMass = ([-0.037242 0 0]);
tail.Inertia = ([26.200 90.288 88.363 0 0 -0.104]);
addVisual(tail,"Mesh","meshes\Tail.stl");
addCollision(tail,"Mesh","meshes\Tail.stl");

joint14 = rigidBodyJoint('joint14', 'revolute');
joint14.PositionLimits = [-1.5, 1.5];
joint14.JointAxis = [0 0 1];

setFixedTransform(joint14, tf_normal_dis);

tail.Joint = joint14;

addBody(robot,tail,'link13');

clear i tmpBody linkNumber linkName refBody joint1 joint2 joint14 head link1 link2 tail;
%%
rndconfig = randomConfiguration(robot);
[comLocation,comJac] = centerOfMass(robot, rndconfig);

show(robot, rndconfig);

hold all
plot3(comLocation(1),comLocation(2),comLocation(3),Marker="x",MarkerSize=30,LineWidth=5);

%% 구성 확인
% [comLocation,comJac] = centerOfMass(robot);
% show(robot);
% hold all
% plot3(comLocation(1),comLocation(2),comLocation(3),Marker="x",MarkerSize=30,LineWidth=5);
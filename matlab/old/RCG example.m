clear;
clc;

%% 모델링 재구성 예제
exmaple_joint = rigidBodyJoint('jnt');

tf_base = trvec2tform([0 0 0]) * eul2tform([0 0 0]) % Base 좌표계

tf_zero_disp = trvec2tform([0 0.3 0.25]) % 원점의 좌표가 잘못된 경우.
tf_zero_orient = eul2tform([-pi pi/2 0]) % 원점의 회전이 잘못된 경우.

tf_correction = tf_zero_disp * tf_zero_orient; % 수정된 좌표계

setFixedTransform(tf_correction) % 수정된 좌표계를 조인트에 적용

%% Robot 구성 시작
robot = rigidBodyTree;
% robot.BaseName = 'base_link';
robot.DataFormat = 'row';

%% Head 링크 구성 정보
tf1 = trvec2tform([0 0 0]); %tf1 translation (xyz)

head = rigidBody('head');
head.Mass = 0.116;
head.CenterOfMass = ([-0.015586 0 0]);
head.Inertia = ([36.629 68.617 68.958 0 0 0.342]);
addVisual(head,"Mesh","C:\Users\Bong\project\snake_RL\matlab\meshes\head.stl", eul2tform([0 0 pi]));
addCollision(head,"Mesh","C:\Users\Bong\project\snake_RL\matlab\meshes\head.stl", eul2tform([0 0 pi]));
% addVisual(head,"Mesh","C:\Users\Bong\project\snake_RL\matlab\meshes\head.dae");

joint1 = rigidBodyJoint('joint1', 'revolute');
joint1.PositionLimits = [-1.5, 1.5];
joint1.JointAxis = [0 1 0];

setFixedTransform(joint1,tf1);

head.Joint = joint1;

addBody(robot,head,"base_link");
%% link1 링크 구성 정보
tf2 = trvec2tform([-0.0685 0 0 ]);

link1 = rigidBody('link1');
link1.Mass = 0.124;
link1.CenterOfMass = ([-0.017735 0 0]);
link1.Inertia = ([39.160 89.971 90.872 0 -0.342 0]);
addVisual(link1,"Mesh","C:\Users\Bong\project\snake_RL\matlab\meshes\link1.stl");
addCollision(link1,"Mesh","C:\Users\Bong\project\snake_RL\matlab\meshes\link1.stl");

joint2 = rigidBodyJoint('joint2', 'revolute');
joint2.PositionLimits = [-1.5, 1.5];
joint2.JointAxis = [0 0 1];

setFixedTransform(joint2, tf2)

link1.Joint = joint2;

addBody(robot,link1,'head');
%% link2 링크 구성 정보
tf3 = trvec2tform([-0.0685 0 0 ]);

link2 = rigidBody('link2');
link2.Mass = 0.124;
link2.CenterOfMass = ([-0.017652 0 0]);
link2.Inertia = ([39.160 90.272 89.371 0 0 0.342]);
addVisual(link2,"Mesh","C:\Users\Bong\project\snake_RL\matlab\meshes\link2.stl", eul2tform([0 0 pi]));
addCollision(link2,"Mesh","C:\Users\Bong\project\snake_RL\matlab\meshes\link2.stl", eul2tform([0 0 pi]));

joint3 = rigidBodyJoint('joint3', 'revolute');
joint3.PositionLimits = [-1.5, 1.5];
joint3.JointAxis = [0 1 0];

setFixedTransform(joint3, tf3)

link2.Joint = joint3;

addBody(robot,link2,'link1');
%% link3 링크 구성 정보
tf4 = trvec2tform([-0.0685 0 0 ]);

link3 = rigidBody('link3');
link3.Mass = 0.124;
link3.CenterOfMass = ([-0.017735 0 0]);
link3.Inertia = ([39.160 89.971 90.872 0 -0.342 0]);
addVisual(link3,"Mesh","C:\Users\Bong\project\snake_RL\matlab\meshes\link1.stl");
addCollision(link3,"Mesh","C:\Users\Bong\project\snake_RL\matlab\meshes\link1.stl");

joint4 = rigidBodyJoint('joint4', 'revolute');
joint4.PositionLimits = [-1.5, 1.5];
joint4.JointAxis = [0 0 1];

setFixedTransform(joint4, tf4)

link3.Joint = joint4;

addBody(robot,link3,'link2');
%% link4 링크 구성 정보
tf5 = trvec2tform([-0.0685 0 0 ]);

link4 = rigidBody('link4');
link4.Mass = 0.124;
link4.CenterOfMass = ([-0.017652 0 0]);
link4.Inertia = ([39.160 90.272 89.371 0 0 0.342]);
addVisual(link4,"Mesh","C:\Users\Bong\project\snake_RL\matlab\meshes\link2.stl", eul2tform([0 0 pi]));
addCollision(link4,"Mesh","C:\Users\Bong\project\snake_RL\matlab\meshes\link2.stl", eul2tform([0 0 pi]));

joint5 = rigidBodyJoint('joint5', 'revolute');
joint5.PositionLimits = [-1.5, 1.5];
joint5.JointAxis = [0 1 0];

setFixedTransform(joint5, tf5)

link4.Joint = joint5;

addBody(robot,link4,'link3');
%% 추가 자동 구성

for i=0:1:0
    if mod(i,2) == 0
        refBody = getBody(robot,"link1");

        tmpBody = copy(refBody);

        linkNumber = 5 + i;
        linkName = 'link' + string(linkNumber);

        tmpBody.Name = linkName;
        tmpBody.Joint.Name = 'joint' + string(linkNumber + 1);

        addBody(robot,tmpBody, 'link' + string(linkNumber - 1));
     
    else    
        refBody = getBody(robot,"link2");

        tmpBody = copy(refBody);

        linkNumber = 5 + i;
        linkName = 'link' + string(linkNumber);

        tmpBody.Name = linkName;
        tmpBody.Joint.Name = 'joint' + string(linkNumber + 1);

        addBody(robot,tmpBody, 'link' + string(linkNumber - 1));
    end

end

show(robot)
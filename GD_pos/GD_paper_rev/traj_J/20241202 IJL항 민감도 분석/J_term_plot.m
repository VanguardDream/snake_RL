clc; clear;
%%
% load J_hist_map2_.mat
load J_maps.mat

total_map = [
    map1(101,:,:);
    map1(94,:,:);
    map1(93,:,:);
    map1(87,:,:);
    map1(86,:,:);
    map1(85,:,:);
    map1(84,:,:);
    map1(80,:,:);
    map1(78,:,:);
    map1(75,:,:);
    map1(73,:,:);
    map1(70,:,:);
    map1(64,:,:);
    map1(61,:,:);
    map1(57,:,:);
    map1(50,:,:);
    map1(49,:,:);
    map1(47,:,:);
    map1(43,:,:);
    map1(41,:,:);
    map1(40,:,:);
    map1(36,:,:);
    map1(35,:,:);
    map1(34,:,:);
    map1(33,:,:);
    map1(32,:,:);
    map1(31,:,:);
    map1(29,:,:);
    map1(28,:,:);
    map1(27,:,:);
    map1( 9,:,:);
    map1( 7,:,:);
    map1( 6,:,:);
    map1( 5,:,:);
    map1( 4,:,:);
    map1( 3,:,:);
    map1( 2,:,:);
    map1( 1,:,:);
    map2(78,:,:); %2 시작
    map2(68,:,:);
    map2(62,:,:);
    map2(59,:,:);
    map2(47,:,:);
    map2(96,:,:);
    map2(95,:,:);
    map2(94,:,:);
    map2(93,:,:);
    map2(92,:,:);
    map2(91,:,:);
    map2(73,:,:);
    map2(72,:,:);
    map2(67,:,:);
    map2(56,:,:);
    map2( 2,:,:);
];
%%
canvas = zeros(500,500);
num_datasets = 101;
data_idx = 1:num_datasets;
for i=data_idx
    for x=1:size(squeeze(U_result(i,:,:)),1)
        for y=1:size(squeeze(U_result(i,:,:)),2)

            if U_result(i,x,y) ~= 0
                canvas(x,y) = i;
            end
        end
    end
end

%%
canvas2 = zeros(500,500);
num_datasets = 54;
data_idx = 1:num_datasets;

for i = data_idx
    canvas2 = canvas2 + squeeze(U_result(i,:,:));
end

%%
mycolor = jet(17);
figure;

s = pcolor(canvas2);
s.EdgeColor = 'none';

xlabel("I term weight","FontSize",13,"FontName","arial","FontWeight","bold");

xlim([1 500]);
ylim([1 500]);

pbaspect([1 1 1])

%%
for i = data_idx
    figure;
    s = pcolor(squeeze(total_map(i,:,:)));
    s.EdgeColor = 'none';
end
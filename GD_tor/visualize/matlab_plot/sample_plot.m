clc; clear;

%%
x = rand([4000 1]);
y = rand([4000 1]);

sample = [x y];

scatter(sample(:,1),sample(:,2),12,"filled")
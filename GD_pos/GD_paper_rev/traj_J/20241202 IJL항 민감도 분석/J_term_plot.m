clc; clear;
%%
load J_hist_map_.mat
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
num_datasets = 101;
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
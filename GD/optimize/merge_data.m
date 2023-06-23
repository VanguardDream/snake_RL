clc; clear;

%% check mat file list

file_struct = dir("*.mat");
file_names = {file_struct.name};

%% load mat file
merge_done = [];
merge_value = [];
merge_vector = [];

for i = 1:length(file_names)
    data = load(string(file_names(i)));

    merge_done = [merge_done; data.result_done];
    merge_value = [merge_value; data.result_value];
    merge_vector = [merge_vector; data.result_vector];
end

%% make as table

total_data = table(merge_done, merge_value, merge_vector);
total_data = sortrows(total_data,2);

% result.done = total_data.merge_done;
% result.value = total_data.merge_value;
% result.vector = total_data.merge_vector;
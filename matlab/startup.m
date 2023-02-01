clc; clear;

%% Load conda env
pyExec = 'C:\Users\doore\anaconda3\envs\rllib\python.exe';
pyRoot = fileparts(pyExec);
p = getenv('PATH');
p = strsplit(p, ';');
addToPath = {
    pyRoot
    fullfile(pyRoot, 'Library', 'mingw-w64', 'bin')
    fullfile(pyRoot, 'Library', 'usr', 'bin')
    fullfile(pyRoot, 'Library', 'bin')
    fullfile(pyRoot, 'Scripts')
    fullfile(pyRoot, 'bin')
    };
p = [addToPath(:); p(:)];
p = unique(p, 'stable');
p = strjoin(p, ';');
setenv('PATH', p);


%% 
% if count(py.sys.path,'') == 0 
%     insert(py.sys.path,int32(0),''); 
% end 

pyreload();

[filename, filepath] = uigetfile('*.xml');
xmlpath = py.interfaces.getpath(filename, filepath);
clear filename, filepath;

% py.interfaces.simstart(xmlpath)

f = parfeval(backgroundPool, @py.interfaces.simstart, 1, xmlpath);

print("done")

% pyrunfile('interfaces.py')
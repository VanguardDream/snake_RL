function pyreload()
    clear classes
    m = py.importlib.import_module('interfaces');
    py.importlib.reload(m);
end
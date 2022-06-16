import numpy as np

def writeToCSV(gait : list, data : np.ndarray):
    import csv
    import datetime

    _now = datetime.datetime.now()
    _now_string = _now.strftime('%Y-%m-%d-%H:%M:%S')

    _file = open('data.csv','a',newline='')
    _writer = csv.writer(_file)

    for _ in range(data.shape[0]):
        if _ == 0:
            _writer.writerow([_now_string] + gait + data[_,:].tolist())
        else:
            _writer.writerow(["----"] + gait + data[_,:].tolist())

    _file.close()
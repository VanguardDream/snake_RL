# © 2021 Bongsub Song <doorebong@gmail.com>
# All right reserved
# Description : Snake robot dynamics SVM-util code

from typing import Dict
import numpy as np
import scipy.io as io

def writeToCSV(gait : list, data : np.ndarray):
    """
    This method is not recommended cause size of data file.
    """
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

def writeToMAT(gait : list, data : np.ndarray):
    """
    Write file to MATLAB MAT format.
    """

    import datetime
    _now = datetime.datetime.now()
    _now_str = _now.strftime('%Y-%m-%d-%H:%M:%S')

    # String processing
    key_str = str(gait)
    
    key_str = key_str.replace('[','')
    key_str = key_str.replace(']','')
    key_str = key_str.replace(',','')
    key_str = key_str.replace('-','m')
    key_str = key_str.replace(' ','_')

    key_paired_data = data

    # Dictionary Key duplicated check
    try:
        datadic = io.loadmat('data.mat')
    except:
        print('Is there MAT file?')
        datadic = dict()


    if key_str in datadic.keys():
        print("Key duplication Exception! at gait vector : " + str(gait))
        return

    datadic["g"+key_str] = key_paired_data
    datadic["Last_time"] = _now_str

    io.savemat("data.mat",datadic)

def writeToMATeach(gait : list, data : np.ndarray):
    """
    Write file to MATLAB MAT format.
    """

    # String processing
    key_str = str(gait)
    
    key_str = key_str.replace('[','')
    key_str = key_str.replace(']','')
    key_str = key_str.replace(',','')
    key_str = key_str.replace('-','m')
    key_str = key_str.replace(' ','_')

    key_paired_data = data

    datadic = dict()

    datadic["g"+key_str] = key_paired_data

    io.savemat("./data/" + "g" + key_str +".mat",datadic)



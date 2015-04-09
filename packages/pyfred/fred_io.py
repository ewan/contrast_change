'''
Created on 2015-04-09

@author: emd
'''

import numpy as np

def fileid_to_fred_fl(fileid):
    return fileid + ".frd"

def write_fred(fred, fred_fl):
    np.savetxt(fred_fl, fred)

def read_fred(fred_fl):
    return np.loadtxt(fred_fl)
'''
Created on 2015-04-09

@author: emd
'''

import pandas as pd

def write_fval_rep(fval_fl, fval_rep, other_columns):
    fval_table = other_columns.join(pd.DataFrame(fval_rep, columns=["X0"]))
    fval_table.to_csv(fval_fl, index=False)

def fileid_to_fval_fl(fileid):
    return fileid + ".rep"
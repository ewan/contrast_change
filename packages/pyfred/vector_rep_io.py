'''
Created on 2015-04-09

@author: emd
'''
import pandas as pd
import os.path as osp

def is_rep_column_name(cn):
    return cn[0] == "X"

def which_rep_columns(column_names):
    return column_names.map(is_rep_column_name)

def read_vector_rep(vector_fl):
    raw_table = pd.read_csv(vector_fl)
    rep_columns = which_rep_columns(raw_table.columns)
    vector_rep = raw_table[:,rep_columns].values
    other_columns = raw_table[:,~rep_columns]
    labels = raw_table[:,"label"]
    return vector_rep, other_columns, labels

def vector_fl_to_fileid(vector_fl):
    return osp.splitext(osp.basename(vector_fl))[0]
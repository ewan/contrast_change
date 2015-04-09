'''
Created on 2015-04-09

@author: emd
'''
import os

def make_output_dir(output_dir):
    if os.path.isdir(output_dir):
        return
    os.makedirs(output_dir)
'''
Created on 2015-04-09

@author: emd
'''
import argparse
import sys

from fred import difference_fred
from fval import project_to_fval
from fval_rep_io import write_fval_rep, fileid_to_fval_fl
import os.path as osp
from vector_rep_io import read_vector_rep, vector_fl_to_fileid
from util import make_output_dir


__version__ = '0.0.1'


def create_parser():
    """Return command-line parser."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version='%(prog)s ' +
                        __version__)
    parser.add_argument('--output-dir', help='target output directory')
    parser.add_argument('--plus-labels', help='labels defining positive'
                        'endpoint of fred')
    parser.add_argument('--minus-labels', help='labels defining negative'
                        'direction of fred')
    parser.add_argument('vector_files', help='files containing vector'
                        'representations', nargs='+')
    return parser


def parse_args(arguments):
    """Parse command-line options."""
    parser = create_parser()
    args = parser.parse_args(arguments)
    return args


if __name__ == '__main__':
    args = parse_args(sys.argv[1:])
    
    make_output_dir(args.output_dir)
    
    for vector_fl in args.vector_files:
        fileid = vector_fl_to_fileid(vector_fl)
        vector_rep, other_columns, labels = read_vector_rep(vector_fl)
        fred = difference_fred(vector_rep, labels, args.plus_labels,
                               args.minus_labels)
        fval_rep = project_to_fval(vector_rep, fred)
        fval_fl = osp.join(args.output_dir, fileid_to_fval_fl(fileid))
        write_fval_rep(fval_rep, fval_fl, other_columns)

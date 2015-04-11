'''
Created on 2015-04-09

@author: emd
'''
import argparse
import sys

from fred import select_fred_fn
from fval import select_fval_fn
from fval_rep_io import write_fval_rep, fileid_to_fval_fl
import numpy as np
import os.path as osp
from util import make_output_dir
from vector_rep_io import read_vector_rep, vector_fl_to_fileid


__version__ = '0.0.1'


def create_parser():
    """Return command-line parser."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version='%(prog)s ' +
                        __version__)
    parser.add_argument('--output-dir', help='target output directory')
    aggregation_opts = parser.add_mutually_exclusive_group()
    aggregation_opts.add_argument('--per-file',
                                  help='generate one fred per file',
                                  action='store_true', default=False)
    aggregation_opts.add_argument('--fred-files',
                                  help='generate fred by aggregating '
                                  'only within the listed files', default=None)
    parser.add_argument('--plus-labels', help='labels defining positive'
                        'endpoint of fred')
    parser.add_argument('--minus-labels', help='labels defining negative'
                        'endpoint of fred')
    parser.add_argument('--plus-covariance-labels', help='labels defining '
                        'positive covariance of fred (lda)', default=None)
    parser.add_argument('--minus-covariance-labels', help='labels defining '
                        'negative covariance of fred (lda)', default=None)
    parser.add_argument('--fred-type', help='type of fred to compute'
                        '(available options: difference, anchor)',
                        default="difference")
    parser.add_argument('vector_files', help='files containing vector'
                        'representations', nargs='+')
    return parser


def parse_args(arguments):
    """Parse command-line options."""
    parser = create_parser()
    args = parser.parse_args(arguments)
    if args.fred_files is not None:
        args.fred_files = args.fred_files.split()
    return args


if __name__ == '__main__':
    args = parse_args(sys.argv[1:])

    fred_fn = select_fred_fn(args.fred_type)
    fval_fn = select_fval_fn(args.fred_type)

    make_output_dir(args.output_dir)

    if args.per_file:
        for vector_fl in args.vector_files:
            fileid = vector_fl_to_fileid(vector_fl)
            vector_rep, other_columns, labels = read_vector_rep(vector_fl)
            fred = fred_fn(vector_rep, labels, args)
            fval_rep = fval_fn(vector_rep, fred)
            fval_fl = osp.join(args.output_dir, fileid_to_fval_fl(fileid))
            write_fval_rep(fval_fl, fval_rep, other_columns)
    else:
        agg_vector_rep = None
        agg_labels = np.array([])
        if args.fred_files is not None:
            fred_files = args.fred_files
        else:
            fred_files = args.vector_files
        for vector_fl in fred_files:
            fileid = vector_fl_to_fileid(vector_fl)
            vector_rep, _, labels = read_vector_rep(vector_fl)
            if agg_vector_rep is None:
                agg_vector_rep = vector_rep
            else:
                agg_vector_rep = np.append(agg_vector_rep, vector_rep, axis=0)
            agg_labels = np.append(agg_labels, labels)
        fred = fred_fn(agg_vector_rep, agg_labels, args)
        for vector_fl in args.vector_files:
            fileid = vector_fl_to_fileid(vector_fl)
            vector_rep, other_columns, _ = read_vector_rep(vector_fl)
            fval_rep = fval_fn(vector_rep, fred)
            fval_fl = osp.join(args.output_dir, fileid_to_fval_fl(fileid))
            write_fval_rep(fval_fl, fval_rep, other_columns)

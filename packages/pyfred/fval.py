import argparse
import sys

from fred_io import read_fred, fileid_to_fred_fl
from fval_rep_io import fileid_to_fval_fl, write_fval_rep
import numpy as np
import os.path as osp
from util import make_output_dir
from vector_rep_io import vector_fl_to_fileid, read_vector_rep


__version__ = '0.0.1'


def scalar_projections(vector_rep, fred):
    return vector_rep.dot(fred)


def euclidean_distances(vector_rep, fred):
    return np.linalg.norm(vector_rep - fred, axis=1, ord=2)


def select_fval_fn(fred_type):
    if fred_type == "difference":
        return scalar_projections
    elif fred_type == "anchor":
        return euclidean_distances


def create_parser():
    """Return command-line parser."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version='%(prog)s ' +
                        __version__)
    parser.add_argument('--fred-dir', help='directory containing freds')
    parser.add_argument('--output-dir', help='target output directory')
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
    return args


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])

    fval_fn = select_fval_fn(args.fred_type)

    make_output_dir(args.output_dir)

    for vector_fl in args.vector_files:
        fileid = vector_fl_to_fileid(vector_fl)
        vector_rep, other_columns, _ = read_vector_rep(vector_fl)
        fred_fl = osp.join(args.fred_dir, fileid_to_fred_fl(fileid))
        fred = read_fred(fred_fl)
        fval_rep = fval_fn(vector_rep, fred)
        fval_fl = osp.join(args.output_dir, fileid_to_fval_fl(fileid))
        write_fval_rep(fval_fl, fval_rep, other_columns)

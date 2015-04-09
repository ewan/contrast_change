import sys
import numpy as np
import argparse
import os.path as osp
from util import make_output_dir
from vector_rep_io import vector_fl_to_fileid, read_vector_rep
from fred_io import fileid_to_fred_fl, write_fred

__version__ = '0.0.1'


def difference_fred(vector_rep, labels, plus_labels, minus_labels):
    plus_indices = [v in plus_labels for v in labels]
    minus_indices = [v in minus_labels for v in labels]
    mn_plus = vector_rep.ix[plus_indices, :].mean()
    mn_minus = vector_rep.ix[minus_indices, :].mean()
    cvector_unnorm = (mn_plus - mn_minus).values
    result = cvector_unnorm / np.linalg.norm(cvector_unnorm)
    return result


def create_parser():
    """Return command-line parser."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version='%(prog)s ' +
                        __version__)
    parser.add_argument('--output-dir', help='target output directory')
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

    make_output_dir(args.output_dir)

    for vector_fl in args.vector_files:
        fileid = vector_fl_to_fileid(vector_fl)
        vector_rep, _, labels = read_vector_rep(vector_fl)
        fred = difference_fred(vector_rep, labels, args.plus_labels,
                               args.minus_labels)
        fred_fl = osp.join(args.output_dir, fileid_to_fred_fl(fileid))
        write_fred(fred, fred_fl)


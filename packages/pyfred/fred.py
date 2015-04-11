import sys
import numpy as np
import argparse
import os.path as osp
from util import make_output_dir
from vector_rep_io import vector_fl_to_fileid, read_vector_rep
from fred_io import fileid_to_fred_fl, write_fred

__version__ = '0.0.1'


def difference_fred(vector_rep, labels, plus_labels, minus_labels):
    plus_indices = np.array([v in plus_labels for v in labels])
    minus_indices = np.array([v in minus_labels for v in labels])
    mn_plus = vector_rep[plus_indices, :].mean(axis=0)
    mn_minus = vector_rep[minus_indices, :].mean(axis=0)
    cvector_unnorm = mn_plus - mn_minus
    result = cvector_unnorm / np.linalg.norm(cvector_unnorm)
    return result


def lda_fred(vector_rep, labels, plus_loc_labels, minus_loc_labels,
             plus_cov_labels, minus_cov_labels):
    plus_loc_indices = np.array([v in plus_loc_labels for v in labels])
    minus_loc_indices = np.array([v in minus_loc_labels for v in labels])
    x_p_l, x_m_l = vector_rep[
        plus_loc_indices, :], vector_rep[minus_loc_indices, :]
    mn_p, mn_m = x_p_l.mean(axis=0), x_m_l.mean(axis=0)
    plus_cov_indices = np.array([v in plus_cov_labels for v in labels])
    minus_cov_indices = np.array([v in minus_cov_labels for v in labels])
    x_p_c, x_m_c = vector_rep[
        plus_cov_indices, :], vector_rep[minus_cov_indices, :]
    cov_p, cov_m = np.cov(x_p_c, rowvar=False), np.cov(x_m_c, rowvar=False)
    scale_mat = np.linalg.inv(cov_p + cov_m)
    fred_unnorm = scale_mat.dot(mn_p - mn_m)
    result = fred_unnorm / np.linalg.norm(fred_unnorm)
    return result


def anchor_fred(vector_rep, labels, anchor_labels):
    anchor_indices = np.array([v in anchor_labels for v in labels])
    return vector_rep[anchor_indices, :].mean(axis=0)


def select_fred_fn(fred_type):
    if fred_type == "difference":
        def f(v, l, args):
            return difference_fred(v, l, args.plus_labels, args.minus_labels)
    elif fred_type == "lda":
        def f(v, l, args):
            if args.plus_covariance_labels is None:
                plus_covariance_labels = args.plus_labels
            else:
                plus_covariance_labels = args.plus_covariance_labels
            if args.minus_covariance_labels is None:
                minus_covariance_labels = args.minus_labels
            else:
                minus_covariance_labels = args.minus_covariance_labels
            return lda_fred(v, l, args.plus_labels, args.minus_labels,
                            plus_covariance_labels, minus_covariance_labels)
    elif fred_type == "anchor":
        def f(v, l, args):
            return anchor_fred(v, l, args.plus_labels)
    return f


def create_parser():
    """Return command-line parser."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--version', action='version', version='%(prog)s ' +
                        __version__)
    parser.add_argument('--output', help='output target filename, or '
                        'directory name if --per-file is set')
    parser.add_argument('--per-file', help='generate one fred per file',
                        action='store_true', default=False)
    parser.add_argument('--plus-labels', help='labels defining positive '
                        'endpoint of fred')
    parser.add_argument('--minus-labels', help='labels defining negative '
                        'direction of fred (difference, lda)')
    parser.add_argument('--plus-covariance-labels', help='labels defining '
                        'positive covariance of fred (lda)', default=None)
    parser.add_argument('--minus-covariance-labels', help='labels defining '
                        'negative covariance of fred (lda)', default=None)
    parser.add_argument('--fred-type', help='type of fred to compute '
                        '(available options: difference, lda, anchor)',
                        default="difference")
    parser.add_argument('vector_files', help='files containing vector '
                        'representations', nargs='+')
    return parser


def parse_args(arguments):
    """Parse command-line options."""
    parser = create_parser()
    args = parser.parse_args(arguments)
    return args


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])

    fred_fn = select_fred_fn(args.fred_type)

    if args.per_file:
        make_output_dir(args.output)
        for vector_fl in args.vector_files:
            fileid = vector_fl_to_fileid(vector_fl)
            vector_rep, _, labels = read_vector_rep(vector_fl)
            fred = fred_fn(vector_rep, labels, args)
            fred_fl = osp.join(args.output, fileid_to_fred_fl(fileid))
            write_fred(fred_fl, fred)
    else:
        vector_rep = None
        labels = np.array([])
        for vector_fl in args.vector_files:
            fileid = vector_fl_to_fileid(vector_fl)
            vector_rep_v, _, labels_v = read_vector_rep(vector_fl)
            if vector_rep is None:
                vector_rep = vector_rep_v
            else:
                vector_rep = np.append(vector_rep, vector_rep_v, axis=0)
            labels = np.append(labels, labels_v)
        fred = fred_fn(vector_rep, labels, args)
        write_fred(args.output, fred)

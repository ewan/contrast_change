import sys
import numpy as np
import pandas as pd

if __name__ == "__main__":
    rep_fn = sys.argv[1]
    contrast_vector_fn = sys.argv[2]
    
    full_table = pd.read_csv(rep_fn, sep=None, engine='python')
    meta_cols = [cn for cn in full_table.columns if cn[0] != "X"]
    meta_table = full_table.ix[:,meta_cols]
    rep_cols = [cn for cn in full_table.columns if cn[0] == "X"]
    rep_table = full_table.ix[:,rep_cols]

    contrast_vector = np.loadtxt(contrast_vector_fn)

    proj = rep_table.values.dot(contrast_vector)
    meta_table["X0"] = proj

    print meta_table.to_csv(index=False)

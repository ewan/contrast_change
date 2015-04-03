import sys
import numpy as np
import pandas as pd

if __name__ == "__main__":
    rep_fn = sys.argv[1]
    plus_values = sys.argv[2]
    minus_values = sys.argv[3]
    
    full_table = pd.read_csv(rep_fn, sep=None, engine='python')
    rep_cols = [cn for cn in full_table.columns if cn[0] == "X"]
    rep_table = full_table.ix[:,rep_cols]

    labels = full_table['v']
    plus_indices = [v in plus_values for v in labels]
    minus_indices = [v in minus_values for v in labels]

    mn_plus = rep_table.ix[plus_indices,:].mean()
    mn_minus = rep_table.ix[minus_indices,:].mean()

    cvector_unnorm = (mn_plus - mn_minus).values
    cvector = cvector_unnorm/np.linalg.norm(cvector_unnorm)

    np.savetxt(sys.stdout, cvector)

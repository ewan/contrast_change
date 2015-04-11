# contrast_change

Study historical change by projecting vector representations along some
dimension, defined by some contrast between two sets of phones.

*reps* contains various sample representations taken from a small corpus of
Canadian English

*analysis/vowel_example.Rmd* is an R markdown document that can be knit to
display various vowels of interest in each of these representations. This
requires ggplot2 and the rphonch package, which is found in
*packages/rphonch_0.0.0.9000.tar.gz*.

To generate representations of this kind (fval representations) from a corpus,
use *packages/pyfred/construct_fvals.py*. The source features
(vector representation) should be stored as csv files, with the feature columns
identified by a leading 'X'; the output fval filenames will be the 
source file name stems (the file name up to the first '.'), and rphonch will
interpret the fval file name stems as a speaker id.
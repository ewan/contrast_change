read_rep <- function(fn) {
  result <- read.csv(fn)
  sid <- strsplit(basename(fn), ".", fixed=T)[[1]][1]
  result$speaker_id <- sid
  return(result)
}

split_vowel_and_stress <- function(d) {
  v_orig <- d %$% as.character(v)
  phoneme <- sub("[[:digit:]]$", "", v_orig)
  stress_raw <- sub("^[[:alpha:]]+", "", v_orig)
  stress <- rep("", length(stress_raw))
  stress[nchar(stress_raw) == 0] <- NA
  stress[nchar(stress_raw) > 0] <- paste0("S", stress_raw[nchar(stress_raw)>0])
  result <- d
  result$phoneme <- phoneme
  result$stress <- stress
  return(result)
}
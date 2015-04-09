normalize_to <- function(pos, neg, d) {
  result <- d
  pos_val <- d[d$phoneme %in% pos,] %$% median(X0)
  neg_val <- d[d$phoneme %in% neg,] %$% median(X0)
  result$X0 <- (d$X0-neg_val)/(pos_val-neg_val)
  return(result)
}

data_split_with_var_subset <- function(d, var_to_check_subset, prop, seed) {
  n_train <- round(prop*nrow(d))
  n_val <- nrow(d) - n_train  
  
  set.seed(seed)
  good_sample <- FALSE
  while (!good_sample) {
    train_ix <- 1:nrow(d) %in% sample(nrow(d), n_train)
    val_ix <- !train_ix
    d_train <- d[train_ix,]
    d_val <- d[val_ix,]    
    train_var <- unique(d_train[[var_to_check_subset]])
    val_var <- unique(d_val[[var_to_check_subset]])
    good_sample <- prod(val_var %in% train_var)
  }
  set.seed(NULL)  
  
  result <- list(d_train, d_val)
}
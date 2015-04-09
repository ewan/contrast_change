library(reshape)

extract_to_data_frame <- function(model, variables, inc_warmup=FALSE) {
  m_vars <- extract(model, variables, permuted=FALSE, inc_warmup=inc_warmup)
  l_chains <- list()
  for (i in 1:dim(m_vars)[2]) {
    l_chains[[i]] <- as.data.frame(m_vars[,i,])
    l_chains[[i]]$iteration <- 1:nrow(l_chains[[i]])
    l_chains[[i]]$chain <- paste0("c", i)
    if (dim(m_vars)[3] == 1) {
      names(l_chains[[i]])[1] <- variables
    }
  }
  d <- do.call("rbind", l_chains)
  result <- melt(d, id.vars=c("iteration", "chain"))
  return(split_vector_var(result))
}

split_vector_var <- function(d) {
  result <- d
  d_variable_c <- as.character(d$variable)
  variable <- d_variable_c
  variable_index <- rep(NA, length(variable))
  has_index <- grepl("\\[[[:digit:]]+\\]$", d_variable_c)
  variable[has_index] <- sapply(strsplit(d_variable_c[has_index],
                                        "\\[[[:digit:]]+\\]$"),
                               function(x) x[1])
  variable_index[has_index] <- as.integer(gsub(".*\\[([[:digit:]]+)\\].*",
                                               "\\1",
                                               d_variable_c[has_index]))
  result$variable <- variable
  result$variable_index <- variable_index
  return(result)
}


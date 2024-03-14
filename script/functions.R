include_libraries <- function(){
  library(methods, quietly = TRUE)
  library(tibble)
  library(rjson)
  library(jsonlite, warn.conflicts = FALSE)
  library(xlsx)
  library(readxl)
  library(psych)
}

prepare_data_of_two <- function(data, group_var) {
  group_names <- c()

  if (data$group_name_1 == data$group_name_2) {
    index = 1
    data$group_name_2 <- paste(data$group_name_2, '_', index)
  }

  for (item in data$group_data_1[[ 1 ]]) {    
      group_names <- append(group_names, data$group_name_1)
  }
  for (item in data$group_data_2[[ 1 ]]) {
      group_names <- append(group_names, data$group_name_2)
  }

  groups <- list()
  groups[[ group_var ]] <- group_names

  scales <- names(data$group_data_1)
  for (scale in scales) {
      values <- c()
      persons <- names(data$group_data_1[[ scale ]])
      for (person in persons) {
          if (is.na(as.numeric(data$group_data_1[[ scale ]][[ person ]]))) {
              values[[ person ]] <- 0;
          } else {
              values[[ person ]] <- data$group_data_1[[ scale ]][[ person ]]
          }
      }
      groups[[ scale ]] <- append(groups[[ scale ]], values)

      values <- c()
      persons <- names(data$group_data_2[[ scale ]])
      for (person in persons) {
          if (is.na(as.numeric(data$group_data_2[[ scale ]][[ person ]]))) {
              values[[ person ]] <- 0;
          } else {
              values[[ person ]] <- data$group_data_2[[ scale ]][[ person ]]
          }
      }
      groups[[ scale ]] <- append(groups[[ scale ]], values)
  }

  main_tibble <- as_tibble(groups)

  return(main_tibble)
}

get_group_var <- function(name, g_name_1, g_name_2) {
  if (g_name_1 == g_name_2) {
    index <- 1
    g_name_2 <- paste(g_name_2, '_', index, sep='')
    index <- index + 1;
  }

  res <- c(name, g_name_1, g_name_2)
  names(res) <- c('name', 'g_name_1', 'g_name_2')

  return(res)
}

text_rand <- function(x, y, z){
  rand <- c(x, y, z)
  rand[round(runif(1, 1, length(rand)), 0)]
}

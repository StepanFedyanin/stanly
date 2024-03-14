calc_prepare_data <- function(data, group_var) {
  group_names <- c()
  for (item in data$group_data_1[[ 1 ]]) {    
      group_names <- append(group_names, data$group_name_1)
  }

  groups <- list()

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
  }


  main_tibble <- as_tibble(groups)

  return(main_tibble)
}

calc_xlsx_main <- function(MAIN_DF, xlsx_file, METHOD_NAME="spearman") {
  MAIN_DF_NAMES <- names(MAIN_DF)

  #нужны все данные или только значимые (если F - то только значимые взаимосвязи)?
  need_all_data <- T

  ###############################
  ####создают пустую матрицу и записываю в нее значения криетрия
  t_stat <- matrix(NA, nrow = length(MAIN_DF_NAMES), ncol = length(MAIN_DF_NAMES))
  for (i in 1:ncol(MAIN_DF)){
    for(j in 1:ncol(MAIN_DF)){
    cor_test <- cor.test(MAIN_DF[[i]], MAIN_DF[[j]], method = METHOD_NAME)
    t_stat[i,j] <- round(cor_test$estimate,3)
    }
  }
  t_stat[row(t_stat) == col(t_stat)] <- NA
  lower.tri(t_stat)
  t_stat[lower.tri(t_stat)] <- NA

  ####создают пустую матрицу и записываю в нее уровень значимости критерия
  t_p_val <- matrix(NA, nrow = length(MAIN_DF_NAMES), ncol = length(MAIN_DF_NAMES))

  for (i in 1:ncol(MAIN_DF)){
    for(j in 1:ncol(MAIN_DF)){
      cor_test <- cor.test(MAIN_DF[[i]], MAIN_DF[[j]], method = METHOD_NAME)
      t_p_val[i,j] <- cor_test$p.value
    }
  }
  t_p_val[row(t_p_val) == col(t_p_val)] <- NA
  lower.tri(t_p_val)
  t_p_val[lower.tri(t_p_val)] <- NA

  ####создают пустую матрицу и записываю в нее ВСЕ корреляции + ставлю звездочки
  t_stat_all_data <- matrix(NA, nrow = length(MAIN_DF_NAMES), ncol = length(MAIN_DF_NAMES))
  for (i in 1:ncol(MAIN_DF)){
    for(j in 1:ncol(MAIN_DF)){
    if(is.na(t_p_val[i,j])){
        NA
      } else if(t_p_val[i,j] <= 0.05 & t_p_val[i,j] > 0.01){
        t_stat_all_data[i,j] <- paste(round(t_stat[i,j],3),"*", sep = "")
      } else if(t_p_val[i,j] <= 0.01 & t_p_val[i,j] > 0.001){
        t_stat_all_data[i,j] <- paste(round(t_stat[i,j],3),"**", sep = "")
      } else if(t_p_val[i,j] <= 0.001 & t_p_val[i,j] > 0){
        t_stat_all_data[i,j] <- paste(round(t_stat[i,j],3),"***", sep = "")
      } else {
        t_stat_all_data[i,j] <- paste(round(t_stat[i,j],3), sep = "")
      }
    }
  }

  ###фирмирую итоговую таблицу со ВСЕМИ корреляциями + если только 2 шкалы свой вывод, если более шкал то свой
  t_need_all_stat_data_length <- t_stat_all_data[!is.na(t_stat_all_data)]

  if(length(t_need_all_stat_data_length) == 1){
    print("1")
    t_need_all_stat_data <- t_stat_all_data
    colnames(t_need_all_stat_data) <- MAIN_DF_NAMES
    rownames(t_need_all_stat_data) <- MAIN_DF_NAMES
    t_need_all_stat_data[is.na(t_need_all_stat_data)] <- ""
  } else {
    print("2")
    t_need_all_stat_data <- t_stat_all_data
    t_need_all_stat_data <- t_need_all_stat_data[rowSums(is.na(t_need_all_stat_data)) != ncol(t_need_all_stat_data),
        colSums(is.na(t_need_all_stat_data)) != nrow(t_need_all_stat_data)]
    colnames(t_need_all_stat_data) <- MAIN_DF_NAMES[2:length(MAIN_DF_NAMES)]
    rownames(t_need_all_stat_data) <- MAIN_DF_NAMES[-length(MAIN_DF_NAMES)]
    #t_need_data <- round(t_need_data, 3)
    t_need_all_stat_data[is.na(t_need_all_stat_data)] <- ""
  }
  write.xlsx(as.data.frame(MAIN_DF, optional = TRUE), file=xlsx_file, col.names=TRUE, row.names=FALSE, sheetName='Входные данные')
  write.xlsx(as.data.frame(t_need_all_stat_data, optional = TRUE), file=xlsx_file, col.names=TRUE, row.names=TRUE, append=TRUE, sheetName='Результат')
}

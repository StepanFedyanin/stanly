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

calc_xlsx_main <- function(MAIN_DF, xlsx_file, stat_sumbol="w") {
  MAIN_DF_SCALE_NAMES <- names(MAIN_DF[,1:ncol(MAIN_DF)])

  #рассчитываю значение криетрия и уровень значимости
  statistic <- NULL
  p_val <- NULL

    for(s in MAIN_DF_SCALE_NAMES){
        result_stat_test <- shapiro.test(as.numeric(MAIN_DF[[s]]))
        statistic_one <- as.numeric(round(result_stat_test$statistic, 3))
          if(is.nan(statistic_one) | is.na(statistic_one)){
            statistic_one <- 1
          }
        statistic <- rbind(statistic, statistic_one)
        p_val_one <- as.numeric(round(result_stat_test$p.value, 3))
          if(is.nan(p_val_one) | is.na(p_val_one)){
            p_val_one <- 1
          }
        p_val <- rbind(p_val, p_val_one)
      }

  ########################анализ уровня значимоти со звездой####################
  p_val_star <- NULL
  for(pv in 1:length(p_val)){
      if(p_val[pv] <= 0.05 & p_val[pv] > 0.01){
          p_val_star[pv] <- paste(p_val[pv],"*", sep = "")
      } else  if(p_val[pv] <= 0.01 & p_val[pv] > 0.001){
          p_val_star[pv] <- paste(p_val[pv],"**", sep = "")
      } else  if(p_val[pv] <= 0.001){
          p_val_star[pv] <- paste(p_val[pv],"***", sep = "")
      } else{
          p_val_star[pv] <- p_val[pv]
      } 
  }
  p_val_star <- as.character(p_val_star)
  #######
  p_val_text <- NULL
  for(pv in 1:length(p_val)){
      if(p_val[pv] <= 0.05 & p_val[pv] > 0.01){
          p_val_text[pv] <- paste("p<0,05", sep = "")
      } else  if(p_val[pv] <= 0.01 & p_val[pv] > 0.001){
          p_val_text[pv] <- paste("p<0,01", sep = "")
      } else  if(p_val[pv] <= 0.001){
          p_val_text[pv] <- paste("p<0,001", sep = "")
      } else{
          p_val_text[pv] <- paste("p>0,05", sep = "")
      } 
  }
  p_val_text <- as.character(p_val_text)
  ######## сохраняю значение критерия и уровень значимости в отдельный дата фрейм
  all_table_names <- data.frame(Name = MAIN_DF_SCALE_NAMES, statistic = statistic, p_val_text = p_val_text)
  names(all_table_names) <- c("Названия шкал", "Значения критерия", "Уровень значимости")
  ##########################Вывод п манна-уитни################################
  result_text_condition <- NULL
  for(pv in 1:length(p_val))
    result_text_condition[pv] <- if(p_val[pv] <= 0.05){
      t_result_1 <- paste("Распределение данных по шкале «",all_table_names[["Названия шкал"]][pv],"» отличается от нормального (",stat_sumbol,"=",all_table_names[["Значения критерия"]][pv],", ",all_table_names[["Уровень значимости"]][pv],").", sep = "")
      t_result_2 <- paste("Текущее распределение данных по шкале «",all_table_names[["Названия шкал"]][pv],"» отличается от нормального (",stat_sumbol,"=",all_table_names[["Значения критерия"]][pv],", ",all_table_names[["Уровень значимости"]][pv],").", sep = "")
      t_result_3 <- paste("По шкале «",all_table_names[["Названия шкал"]][pv],"» распределение данных отличается от нормального (",stat_sumbol,"=",all_table_names[["Значения критерия"]][pv],", ",all_table_names[["Уровень значимости"]][pv],").", sep = "")
      #print(text_rand(t_result_1, t_result_2, t_result_3))    
    } else{
      t_result_1 <- paste("Распределение данных по шкале «",all_table_names[["Названия шкал"]][pv],"» не отличается от нормального (",stat_sumbol,"=",all_table_names[["Значения критерия"]][pv],", ",all_table_names[["Уровень значимости"]][pv],").", sep = "")
      t_result_2 <- paste("Текущее распределение данных по шкале «",all_table_names[["Названия шкал"]][pv],"» не отличается от нормального (",stat_sumbol,"=",all_table_names[["Значения критерия"]][pv],", ",all_table_names[["Уровень значимости"]][pv],").", sep = "")
      t_result_3 <- paste("По шкале «",all_table_names[["Названия шкал"]][pv],"» распределение данных не отличается от нормального (",stat_sumbol,"=",all_table_names[["Значения критерия"]][pv],", ",all_table_names[["Уровень значимости"]][pv],").", sep = "")
      #print(text_rand(t_result_1, t_result_2, t_result_3))  
    } 
  result_text_condition <- as.character(result_text_condition)

  ###выясняю какой метод в итоге нужно использовать
  count_norm <- length(p_val[p_val>0.05])
  count_no_norm <- length(p_val[p_val<=0.05])
  count_norm_text <- ifelse(count_norm > count_no_norm, paste("Количество шкал с нормальным распределением (",count_norm," шкал) больше, чем количество шкал с ненормальным распределением (",count_no_norm," шкал), поэтому будем использовать параметрические методы.", sep = ""), paste("Количество шкал с нормальным распределением (",count_norm," шкал) меньше, чем количество шкал с ненормальным распределением (",count_no_norm," шкал), поэтому будем использовать непараметрические методы.", sep = ""))

  ######################Итоговая таблица со всеми данными#######################
  # сохраняю значение критерия и уровень значимости в отдельный дата фрейм
  all_table <- data.frame(all_table_names[["Названия шкал"]], 
                          as.numeric(statistic), 
                          # as.numeric(p_val), 
                          p_val_star
                          # stat_condition = result_text_condition
                          )
  # colnames(all_table) <- c('Названия шкал', 'W', 'p_value', 'p_value_star')
  colnames(all_table) <- c('Названия шкал', 'W', 'p_value_star')

  write.xlsx(as.data.frame(MAIN_DF, optional = TRUE), file=xlsx_file, col.names=TRUE, row.names=FALSE, sheetName='Входные данные')
  write.xlsx(as.data.frame(all_table, optional = TRUE), file=xlsx_file, col.names=TRUE, row.names=FALSE, append=TRUE, sheetName='Результат')
}

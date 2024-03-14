calc_prepare_data <- function(data) {
  group_names <- c()
  group_quantity <- data$group_quantity

  for (i in 1:group_quantity) {
    for(j in 1:data[[ paste('group_count_', as.character(i), sep="") ]]) {
      group_names <- append(group_names, data[[ paste('group_name_', as.character(i), sep="") ]])
    }
  }

  groups <- list()
  groups[[ 'Группа' ]] <- append(groups[[ 'Группа' ]], group_names)
  scales <- names(data$group_data_1)

  for (scale in scales) {
    for (i in 1:group_quantity) {
      values <- c()
      persons <- names(data[[ paste('group_data_', as.character(i), sep="") ]][[ scale ]])
      for (person in persons) {
        if (is.na(as.numeric(data[[ paste('group_data_', as.character(i), sep="") ]][[ scale ]][[ person ]]))) {
          values[[ person ]] <- 0;
        } else {
          values[[ person ]] <- data[[ paste('group_data_', as.character(i), sep="") ]][[ scale ]][[ person ]]
        }
      }
      groups[[ scale ]] <- append(groups[[ scale ]], values)
    }
  }

  main_tibble <- as_tibble(groups)
  return(main_tibble)
}

calc_kruskal <- function(MAIN_DF, psy_table_names=FALSE) {

  #нахожу название группирующей переменной - это ВСЕГДА первая колонка
  #делаю ее фактором
  GROUP_VAR <- names(MAIN_DF[,1])
  MAIN_DF[[GROUP_VAR]] <- as.factor(MAIN_DF[[GROUP_VAR]])

  # созданию новe. перменную с именами шкал для анализа (без группирующей переменной)
  # и получаю список уровней группирующей переменной
  MAIN_DF_SCALE_NAMES <- names(MAIN_DF[,2:ncol(MAIN_DF)])
  GROUP_VAR_LEVELS <- levels(MAIN_DF[[GROUP_VAR]])

  #убираю из стат. аналиа данные о номерах групп
  MAIN_DF_STAT <- MAIN_DF[,2:ncol(MAIN_DF)]
  ###################### РАСЧЕТ НУЖНЫХ ПОКАЗАТЕЛЕЙ КРИТЕРИЯ #####################
  #Непосредственный расчет статистики критерия
  statistic <- NULL
  p_val <- NULL
  for(s in MAIN_DF_SCALE_NAMES){
      result_stat_test <- kruskal.test(MAIN_DF[[s]] ~ MAIN_DF[[GROUP_VAR]],
                                      data = MAIN_DF)
      statistic_one <- as.numeric(round(result_stat_test$statistic, 3))
      statistic <- rbind(statistic, statistic_one)
      p_val_one <- as.numeric(round(result_stat_test$p.value, 3))
      p_val <- rbind(p_val, p_val_one)
  }

  #анализ уровня значимоти со звездой
  p_val_star <- NULL
  for(pv in 1:length(p_val))
    if(p_val[pv] <= 0.05 & p_val[pv] > 0.01){
      p_val_star[pv] <- paste(p_val[pv],"*", sep = "")
    } else  if(p_val[pv] <= 0.01 & p_val[pv] > 0.001){
      p_val_star[pv] <- paste(p_val[pv],"**", sep = "")
    } else  if(p_val[pv] <= 0.001){
      p_val_star[pv] <- paste(p_val[pv],"***", sep = "")
    } else{
      p_val_star[pv] <- p_val[pv]
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
  # сохраняю значения критерия и уровень значимости в отдельный дата фрейм, чтобы можно было делать выводы
  all_table_names <- data.frame(Name = MAIN_DF_SCALE_NAMES, statistic = statistic, p_val_text = p_val_text)
  names(all_table_names) <- c("Названия шкал", "Значения критерия", "Уровень значимости")
  ##########################ТЕКСТОВЫЙ ВЫВОД ПО КРУСКАЛЛУ-УОЛЛЕСУ ################################
  result_text_condition <- NULL
  for(pv in 1:length(p_val))
    result_text_condition[pv] <- if(p_val[pv] <= 0.05){
      t_result_1 <- paste("Выявлены различия по шкале «",all_table_names[["Названия шкал"]][pv],"» 
                          между исследуемыми группами (H=",all_table_names[["Значения критерия"]][pv],", ",all_table_names[["Уровень значимости"]][pv],").", sep = "")
      t_result_2 <- paste("Между группами существуют значимые различия по шкале «",all_table_names[["Названия шкал"]][pv],"» 
                          (Н=",all_table_names[["Значения критерия"]][pv],", ",all_table_names[["Уровень значимости"]][pv],").  ", sep = "")
      t_result_3 <- paste("Существуют значимые различия по шкале «",all_table_names[["Названия шкал"]][pv],"» 
                          между исследуемыми группами (Н=",all_table_names[["Значения критерия"]][pv],", ",all_table_names[["Уровень значимости"]][pv],").", sep = "")  
      t_result_4 <- paste("Были выявлены значимые различия между группами по шкале «",all_table_names[["Названия шкал"]][pv],"» 
                          (Н=",all_table_names[["Значения критерия"]][pv],", p<0,05).", sep = "")
      print(text_rand(t_result_1, t_result_2, t_result_3))    
    } else{
      paste("Различия по шкале «",all_table_names[["Названия шкал"]][pv],"» не значимы.", sep = "")
    } 
  #######################Рассчитываю СРЕДНИЕ ЗНАЧЕНИЯ ПО ГРУППАм#######################
  mean_group <- NULL
  for(i in MAIN_DF_SCALE_NAMES){ 
    mean_group_one <- round(tapply(MAIN_DF_STAT[[i]], MAIN_DF[[GROUP_VAR]], 
                                            mean, na.rm=TRUE),3)
    mean_group <- rbind(mean_group, mean_group_one)
  }
  row.names(mean_group) <- NULL

  #сохраняю данные в дата фрейм и дополнение информацией о шкалах и уровнях
  mean_group_df <-as.data.frame(t(mean_group))
  names(mean_group_df) <- MAIN_DF_SCALE_NAMES
  mean_group_df["Группы"] <- GROUP_VAR_LEVELS
  #######################ОПРЕДЕЛЕНИЕ - вывод по минимальному-максимальному значению#######################
  condition_max_min <- NULL
  for(l in MAIN_DF_SCALE_NAMES){
    condition_max_min[l] <- paste("Максимальное значение наблюдается в группе «", 
                 mean_group_df["Группы"][which.max(mean_group_df[[l]]), "Группы"],
                 "» (среднее значение = ",mean_group_df[which.max(mean_group_df[[l]]), l],
                 "), минимальное значение в группе «",
                 mean_group_df["Группы"][which.min(mean_group_df[[l]]), "Группы"],
                 "» (среднее значение = ",mean_group_df[which.min(mean_group_df[[l]]), l],
                 ").", sep = "")
  }
  condition_max_min <- as.character(condition_max_min)
  ######Психологический вывод
  result_text_psy_condition <- NULL
  for(pvp in 1:length(p_val)){
    if(psy_table_names != FALSE){
      result_text_psy_condition[pvp] <- if(p_val[pvp] < 0.05){
        t_result_1 <- paste("Наибольшие значения таких психологических феноменов как ",
                            psy_table_names[["Описание"]][pvp],
                            " выявлены в группе «",
                            mean_group_df["Группы"][which.max(mean_group_df[[l]]), "Группы"],
                            "», а наименьшие выявлены в группе «",
                            mean_group_df["Группы"][which.min(mean_group_df[[l]]), "Группы"],"».", 
                            sep = "")
        t_result_2 <- paste("Наибольшие показатели по параметрам ",
                            psy_table_names[["Описание"]][pvp],
                            " наблюдается в группе «",
                            mean_group_df["Группы"][which.max(mean_group_df[[l]]), "Группы"],
                            "», а наименьшее в группе «",
                            mean_group_df["Группы"][which.min(mean_group_df[[l]]), "Группы"],"».", 
                            sep = "")
        t_result_3 <- paste("Такой психологический феномен как ",
                            psy_table_names[["Описание"]][pvp],
                            " наиболее всего выражен в группе «",
                            mean_group_df["Группы"][which.max(mean_group_df[[l]]), "Группы"],
                            "», а наименее всего в группе «",
                            mean_group_df["Группы"][which.min(mean_group_df[[l]]), "Группы"],"».", 
                            sep = "")
        print(text_rand(t_result_1, t_result_2, t_result_3))    
      } else{
        paste("По шкале «",psy_table_names[["Название шкал"]][pvp],
              "» группы не отличается друг от друга.", sep = "")
      } 
    } else{
      result_text_psy_condition[pvp] <- paste("", sep = "")
    }
  }
  result_text_psy_condition <- as.character(result_text_psy_condition)
  #######################ФОРМИРУЮ ЕДИНУЮ ТАБЛИЦУ#######################
  #формирую правильные названия для итоговой таблицы с учетом подстановки текст "Среднее значение в группе ..."
  names_mean_group_df <- NULL
  for(sn in GROUP_VAR_LEVELS){
    names_mean_group_df[sn] <- paste("Среднее значение в группе «",sn,"»", 
                                     sep = "")
  }
  #создаю итоговый дата фрейм
  all_table <- NULL
  all_table <- data.frame(Name = MAIN_DF_SCALE_NAMES, 
                           mean_group, 
                           statistic = as.numeric(statistic), 
                           p_val = as.numeric(p_val), 
                           p_val_star, 
                           result_text_condition, 
                           condition_max_min,
                           result_text_psy_condition)
  return(all_table)
}
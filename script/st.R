# st - STUDENT (DEP and INDEP)

st_base <- function(MAIN_DF, GROUP_VAR, GROUP_1_NAME, GROUP_2_NAME, pair, desc_file=F) {
  # импортирую данные в дата фрейм и основной дата фрейм "MAIN_DF"

  psy_table_names <- FALSE

  if(desc_file != FALSE){
    psy_table_names <- read_excel(paste("../../tmp/desc/", desc_file, sep=''))
  }

  #созданию новую перменную с именами шкал для анализа (без группирующей переменной)
  #и получаю список уровней группирующей переменной
  MAIN_DF_SCALE_NAMES <- names(MAIN_DF[,2:ncol(MAIN_DF)])

  #убираю из стат. аналиа данные о номерах групп
  MAIN_DF_STAT <- MAIN_DF[,2:ncol(MAIN_DF)]

  ####################################
  #рассчитываю средние арифметические в каждой группе
  mean_group <- NULL
  for(i in MAIN_DF_SCALE_NAMES){ 
    mean_group_one <- round(tapply(MAIN_DF_STAT[[i]], MAIN_DF[[GROUP_VAR]], 
                                            mean, na.rm=TRUE),3)
    mean_group <- rbind(mean_group, mean_group_one)
  }

  #ввожу переменную для сохранения ТЕКСТОВ результатов вывода по медиане

  #рассчитываю стандартное отклонение в каждой группе
  sd_group <- NULL
  for(i in MAIN_DF_SCALE_NAMES){ 
    sd_group_one <- round(tapply(MAIN_DF_STAT[[i]], MAIN_DF[[GROUP_VAR]], 
                                            sd, na.rm=TRUE),3)
    sd_group <- rbind(sd_group, sd_group_one)
  }

  #соединяю среднее арифметическое и станадртное отклонение по каждой группе
  Mean_sd_1 = paste(as.numeric(mean_group[,1]),"±",as.numeric(sd_group[,1]), sep = "")
  Mean_sd_2 = paste(as.numeric(mean_group[,2]),"±",as.numeric(sd_group[,2]), sep = "")
  #ввожу переменную для сохранения ТЕКСТОВ результатов вывода по медиане
  mean_text_condition <- NULL
  for(i in 1:length(MAIN_DF_SCALE_NAMES)){
    mean_text_condition[i] <- if(mean_group[i,1] > mean_group[i,2]){
      t_over_1 <- paste("Среднее значение в группе «",GROUP_1_NAME,"» (X =",mean_group[i,1],") больше среднего значения группы «",GROUP_2_NAME,"» (X =",mean_group[i,2],"). ", sep = "")
      t_over_2 <- paste("В группе «",GROUP_1_NAME,"» среднее значение равно ",mean_group[i,1],", это больше среднего значения группы «",GROUP_2_NAME,"» равного ",mean_group[i,2],". ", sep = "")
      t_over_3 <- paste("Среднее значение в группе «",GROUP_1_NAME,"» больше среднего значения группы «",GROUP_2_NAME,"» (X1 =",mean_group[i,1],", X2 =",mean_group[i,2],"). ", sep = "")
      text_rand(t_over_1, t_over_2, t_over_3)
    }else if (mean_group[i,1] < mean_group[i,2]){
      t_less_1 <- paste("Среднее значение в группе «",GROUP_1_NAME,"» (X =",mean_group[i,1],") меньше среднего значения группы «",GROUP_2_NAME,"» (X =",mean_group[i,2],"). ", sep = "")
      t_less_2 <- paste("В группе «",GROUP_1_NAME,"» среднее значение равно ",mean_group[i,1],", это меньше среднего значения группы «",GROUP_2_NAME,"» равного ",mean_group[i,2],". ", sep = "")
      t_less_3 <- paste("Среднее значение в группе «",GROUP_1_NAME,"» меньше среднего значения группы «",GROUP_2_NAME,"» (X1 =",mean_group[i,1],", X2 =",mean_group[i,2],"). ", sep = "")
      text_rand(t_less_1, t_less_2, t_less_3)
    }else {
      t_equal_1 <- paste("Среднее значение в группе «",GROUP_1_NAME,"» (X =",mean_group[i,1],") равна среднему значению группы «",GROUP_2_NAME,"» (X =",mean_group[i,2],"). ", sep = "")
      t_equal_2 <- paste("В группе «",GROUP_1_NAME,"» среднее значение равно ",mean_group[i,1],", что равно среднему значению в группе «",GROUP_2_NAME,"» (",mean_group[i,2],"). ", sep = "")
      t_equal_3 <- paste("Среднее значение в группе «",GROUP_1_NAME,"» равно среднему значению в группе «",GROUP_2_NAME,"» (X1 =",mean_group[i,1],", X2 =",mean_group[i,2],"). ", sep = "")
      text_rand(t_equal_1, t_equal_2, t_equal_3)
    }
  }

  #рассчитываю значение криетрия и уровень значимости
  statistic <- NULL
  p_val <- NULL
  for(s in MAIN_DF_SCALE_NAMES){
      result_stat_test <- t.test(as.numeric(MAIN_DF[[s]]) ~ MAIN_DF[[1]], 
                                    data = MAIN_DF, 
                                    paired = pair, 
                                    exact = F, 
                                    correct = F)
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
  #######
  # сохраняю все среднее арифметическое + значение критерия и уровень значимости в отдельный дата фрейм
  all_table_names <- data.frame(Name = MAIN_DF_SCALE_NAMES, 
                                statistic = statistic, 
                                p_val_text = p_val_text)
  names(all_table_names) <- c("Названия шкал", 
                              "Значения критерия", 
                              "Уровень значимости")
  ##########################Вывод п манна-уитни################################
  result_text_condition <- NULL
  for(pv in 1:length(p_val))
    result_text_condition[pv] <- if(p_val[pv] < 0.05){
      t_result_1 <- paste("Выявлены различия по шкале «",all_table_names[["Названия шкал"]][pv],
                          "» между группой «",GROUP_1_NAME,"» и группой «",GROUP_2_NAME,
                          "» (T=",all_table_names[["Значения критерия"]][pv],", ",
                          all_table_names[["Уровень значимости"]][pv],").", sep = "")
      t_result_2 <- paste("Между группой «",GROUP_1_NAME,"» и группой «",GROUP_2_NAME,
                          "» существуют значимые различия по шкале «",
                          all_table_names[["Названия шкал"]][pv],
                          "» (T=",all_table_names[["Значения критерия"]][pv],", ",
                          all_table_names[["Уровень значимости"]][pv],").", sep = "")
      t_result_3 <- paste("Существуют значимые различия по шкале «",
                          all_table_names[["Названия шкал"]][pv],"» между группой «",
                          GROUP_1_NAME,"» и группой «",GROUP_2_NAME,
                          "» (T=",all_table_names[["Значения критерия"]][pv],", ",
                          all_table_names[["Уровень значимости"]][pv],").", sep = "") 
      t_result_4 <- paste("Были выявлены значимые различия между группой «",GROUP_1_NAME,
                          "» и группой «",GROUP_2_NAME,"» по шкале «",
                          all_table_names[["Названия шкал"]][pv],
                          "» (T=",all_table_names[["Значения критерия"]][pv],", ",
                          all_table_names[["Уровень значимости"]][pv],").", sep = "")
    } else{
      paste("Различия по шкале «",all_table_names[["Названия шкал"]][pv],"» между группой «",GROUP_1_NAME,"» и группой «",GROUP_2_NAME,"» не значимы.", sep = "")
    } 
  result_text_condition <- as.character(result_text_condition)
  ######################Психологическое описание#######################
  ######ПСИХОЛОГИЧЕСКОЕ ОПИСАНИЕ######
  result_text_psy_condition <- NULL
  for(pvp in 1:length(p_val)){
    if(psy_table_names != FALSE){
      result_text_psy_condition[pvp] <- if(p_val[pvp] < 0.05){
        t_result_1 <- paste("Группа «",GROUP_1_NAME,"» отличается от группы «",
                            GROUP_2_NAME,"» ",
                            psy_table_names[["Описание со склонением"]][pvp],
                            ".", sep = "")
        t_result_2 <- ifelse(mean_group[pvp,1] > mean_group[pvp,2],
                             paste("В группе «",GROUP_1_NAME,"» выше ",
                                   psy_table_names[["Описание"]][pvp],
                                   " по сравнению с группой «",GROUP_2_NAME,
                                   "».", sep = ""),
                             paste("В группе «",GROUP_1_NAME,
                                   "» ниже ",psy_table_names[["Описание"]][pvp],
                                   " по сравнению с группой «",GROUP_2_NAME,
                                   "».", sep = ""))
        t_result_3 <- ifelse(mean_group[pvp,1] > mean_group[pvp,2],
                             paste("Такой психологический феномен как ",
                                   psy_table_names[["Описание"]][pvp],
                                   " больше в группе «",GROUP_1_NAME,
                                   "», чем в группе «",GROUP_2_NAME,"».", sep = ""),
                             paste("Такой психологический феномен как ",
                                   psy_table_names[["Описание"]][pvp],
                                   " меньше в группе «",GROUP_1_NAME,
                                   "», чем в группе «",GROUP_2_NAME,"».", sep = ""))
        print(text_rand(t_result_1, t_result_2, t_result_3))    
      } else{
        paste("В группе «",GROUP_1_NAME,"» ",
              psy_table_names[["Описание"]][pvp],
              " не отличается от группы «",
              GROUP_2_NAME,"»", sep = "")
      } 
    } else{
      result_text_psy_condition[pvp] <- paste("", sep = "")
    }
  }
  result_text_psy_condition <- as.character(result_text_psy_condition)

  ######################Итоговая таблица со всеми данными#######################
  # сохраняю все среднее арифметическое + значение критерия и уровень значимости в отдельный дата фрейм
  all_table <- data.frame(Name = all_table_names[["Названия шкал"]], 
                          Mean_1 = Mean_sd_1, 
                          Mean_2 = Mean_sd_2, 
                          U = as.numeric(statistic), 
                          p_value = as.numeric(p_val), 
                          p_value_star = p_val_star, 
                          result_condition = result_text_condition, 
                          condition = mean_text_condition,
                          psy_condition = result_text_psy_condition)

  return(all_table)
}

st <- function(MAIN_DF, GROUP_VAR, GROUP_1_NAME, GROUP_2_NAME, pair, desc_file=NULL) {
  all_table = st_base(MAIN_DF, GROUP_VAR, GROUP_1_NAME, GROUP_2_NAME, pair, desc_file)
  names(all_table) <- c("Названия шкал", 
                        paste("Среднее значение в группе «",GROUP_1_NAME,"»", sep = ""), 
                        paste("Среднее значение в группе «",GROUP_2_NAME,"»", sep = ""), 
                        "Эмпирическое значение критерия", 
                        "Уровень значимости критерия",
                        "Уровень значимости", 
                        "Вывод про уровень значимости", 
                        "Вывод про средние",
                        "Психологический вывод")

  return(all_table)
}

st_xlsx <- function(MAIN_DF, GROUP_VAR, GROUP_1_NAME, GROUP_2_NAME, pair) {
  all_table = st_base(MAIN_DF, GROUP_VAR, GROUP_1_NAME, GROUP_2_NAME, pair)
  return(all_table)
}

st_graph <- function(all_table, MAIN_DF, GROUP_VAR, GROUP_1_NAME, GROUP_2_NAME) {
  if (sum(all_table[["Уровень значимости критерия"]] <= 0.05) != 0){
    for (vr in 1:length(all_table[["Названия шкал"]])){
      if(all_table[["Уровень значимости критерия"]][vr] <= 0.05){
        cat(paste(all_table[["Вывод про уровень значимости"]][vr],
                  " ",all_table[["Психологический вывод"]][vr],
                  " ",all_table[["Вывод про средние"]][vr]))
        cat("\n", sep="\n")
        scale_name <- as.character(all_table[["Названия шкал"]][vr])
        boxplot(MAIN_DF[[scale_name]] ~ MAIN_DF[[GROUP_VAR]], 
                xlab=GROUP_VAR, 
                ylab=scale_name, 
                names=c(GROUP_1_NAME, GROUP_2_NAME),
                cex.axis = 0.4,
                sep = "")
        cat("\n", sep="\n")
      } else {
       NULL
      }
    }
  } else {
      cat("Между группой «",GROUP_1_NAME,"» и группой «",GROUP_2_NAME,"» не было выявлено значимых различий по исследуемым шкалам.", sep = "")
  }
}

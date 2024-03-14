# mww - MANN WHITNEY and WILCOX !

mww <- function(MAIN_DF, GROUP_VAR, GROUP_1_NAME, GROUP_2_NAME, pair, desc_file=F){
  # импортирую данные в дата фрейм и основной дата фрейм "MAIN_DF"
  psy_table_names <- FALSE

  if(desc_file != FALSE){
    psy_table_names <- read_excel(paste("../../tmp/desc/", desc_file, sep=''))
  }

  #созданию новую перменную с именами шкал для анализа (без группирующей переменной)
  #и получаю список уровней группирующей переменной
  MAIN_DF_SCALE_NAMES <- names(MAIN_DF[,2:ncol(MAIN_DF)])

  #нахожу название группирующей переменной - это ВСЕГДА первая колонка
  #делаю ее фактором
  # GROUP_VAR <- names(MAIN_DF[,1])
  MAIN_DF[[GROUP_VAR]] <- as.factor(MAIN_DF[[GROUP_VAR]])

  #созданию новую перменную с именами шкал для анализа (без группирующей переменной)
  #и получаю список уровней группирующей переменной
  MAIN_DF_SCALE_NAMES <- names(MAIN_DF[,2:ncol(MAIN_DF)])

  #убираю из стат. аналиа данные о номерах групп
  MAIN_DF_STAT <- MAIN_DF[,2:ncol(MAIN_DF)]

  GROUP_VAR_LEVELS <- levels(MAIN_DF[[GROUP_VAR]])
  #обозначение первой и второй группы

  #зависимые выборки?
  #если FALSE то считает Манна-Уитни, иначе Т-Вилкосона

  #####################################рассчитываю средние арифметические в каждой группе
  mean_group <- NULL
  for(i in MAIN_DF_SCALE_NAMES){ 
    mean_group_one <- round(tapply(MAIN_DF_STAT[[i]], MAIN_DF[[GROUP_VAR]], 
                                            mean, na.rm=TRUE),3)
    mean_group <- rbind(mean_group, mean_group_one)
  }

  #ввожу переменную для сохранения ТЕКСТОВ результатов вывода по медиане
  mean_text_condition <- NULL
  for(i in 1:length(MAIN_DF_SCALE_NAMES)){
    mean_text_condition[i] <- if(mean_group[i,1] > mean_group[i,2]){
      t_over_1 <- paste("Среднее значение в группе «",GROUP_1_NAME,"» (X=",mean_group[i,1],") больше среднего значения группы «",GROUP_2_NAME,"» (X=",mean_group[i,2],"). ", sep = "")
      t_over_2 <- paste("В группе «",GROUP_1_NAME,"» среднее значение равно ",mean_group[i,1],", это больше среднего значения группы «",GROUP_2_NAME,"» равного ",mean_group[i,2],". ", sep = "")
      t_over_3 <- paste("Показатель в группе «",GROUP_1_NAME,"» выше, чем в группе «",GROUP_2_NAME,"» (X1 =",mean_group[i,1],", X2 =",mean_group[i,2],"). ", sep = "")
      text_rand(t_over_1, t_over_2, t_over_3)
    }else if (mean_group[i,1] < mean_group[i,2]){
      t_less_1 <- paste("Среднее значение в группе «",GROUP_1_NAME,"» (X=",mean_group[i,1],") меньше среднего значения группы «",GROUP_2_NAME,"» (X=",mean_group[i,2],"). ", sep = "")
      t_less_2 <- paste("В группе «",GROUP_1_NAME,"» среднее значение равно ",mean_group[i,1],", это меньше среднего значения группы «",GROUP_2_NAME,"» равного ",mean_group[i,2],". ", sep = "")
      t_less_3 <- paste("Показатель в группе «",GROUP_1_NAME,"» ниже, чем показатель в группе «",GROUP_2_NAME,"» (X1=",mean_group[i,1],", X2=",mean_group[i,2],"). ", sep = "")
      text_rand(t_less_1, t_less_2, t_less_3)
    }else {
      t_equal_1 <- paste("Среднее значение в группе «",GROUP_1_NAME,"» (X=",mean_group[i,1],") равна среднему значению группы «",GROUP_2_NAME,"» (X=",mean_group[i,2],"). ", sep = "")
      t_equal_2 <- paste("В группе «",GROUP_1_NAME,"» среднее значение равно ",mean_group[i,1],", что равно среднему значению в группе «",GROUP_2_NAME,"» (",mean_group[i,2],"). ", sep = "")
      t_equal_3 <- paste("Среднее значение в группе «",GROUP_1_NAME,"» равно среднему значению в группе «",GROUP_2_NAME,"» (X1=",mean_group[i,1],", X2=",mean_group[i,2],"). ", sep = "")
      text_rand(t_equal_1, t_equal_2, t_equal_3)
    }
  }

  #рассчитываю значение криетрия и уровень значимости
  statistic <- NULL
  p_val <- NULL
  for(s in MAIN_DF_SCALE_NAMES){
      result_stat_test <- wilcox.test(as.numeric(MAIN_DF[[s]]) ~ MAIN_DF[[1]], 
                                    data = MAIN_DF, 
                                    paired = pair, 
                                    exact = F, 
                                    correct = F)
      statistic_one <- as.numeric(round(result_stat_test$statistic, 3))
      statistic <- rbind(statistic, statistic_one)
      p_val_one <- as.numeric(round(result_stat_test$p.value, 3))
      p_val_one <- as.numeric(ifelse(is.na(p_val_one),paste("1", sep = ""),p_val_one))
      p_val <- rbind(p_val, p_val_one)
  }

  ########################анализ уровня значимоти со звездой####################
  p_val_star <- NULL
  pv <- 7 
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
  all_table_names <- data.frame(Name = MAIN_DF_SCALE_NAMES, statistic = statistic, p_val_text = p_val_text)
  names(all_table_names) <- c("Названия шкал", "Значения критерия", "Уровень значимости")
  ##########################Вывод п манна-уитни################################
  result_text_condition <- NULL
  for(pv in 1:length(p_val))
    result_text_condition[pv] <- if(p_val[pv] < 0.05){
      t_result_1 <- paste("Выявлены различия по шкале «",all_table_names[["Названия шкал"]][pv],"» между группой «",GROUP_1_NAME,"» и группой «",GROUP_2_NAME,"» (U=",all_table_names[["Значения критерия"]][pv],", ",all_table_names[["Уровень значимости"]][pv],").", sep = "")
      t_result_2 <- paste("Между группой «",GROUP_1_NAME,"» и группой «",GROUP_2_NAME,"» существуют значимые различия по шкале «",all_table_names[["Названия шкал"]][pv],"» (U=",all_table_names[["Значения критерия"]][pv],", ",all_table_names[["Уровень значимости"]][pv],").", sep = "")
      t_result_3 <- paste("Существуют значимые различия по шкале «",all_table_names[["Названия шкал"]][pv],"» между группой «",GROUP_1_NAME,"» и группой «",GROUP_2_NAME,"» (U=",all_table_names[["Значения критерия"]][pv],", ",all_table_names[["Уровень значимости"]][pv],").", sep = "")
      t_result_4 <- paste("Были выявлены значимые различия между группой «",GROUP_1_NAME,"» и группой «",GROUP_2_NAME,"» по шкале «",all_table_names[["Названия шкал"]][pv],"» (U=",all_table_names[["Значения критерия"]][pv],", ",all_table_names[["Уровень значимости"]][pv],").", sep = "")
      print(text_rand(t_result_1, t_result_2, t_result_3))    
    } else{
      paste("Различия по шкале «",all_table_names[["Названия шкал"]][pv],"» между группой «",GROUP_1_NAME,"» и группой «",GROUP_2_NAME,"» не значимы.", sep = "")
    } 
  result_text_condition <- as.character(result_text_condition)

  ######ПСИХОЛОГИЧЕСКОЕ ОПИСАНИЕ######

  result_text_psy_condition <- NULL

  for(pvp in 1:length(p_val)){
    if(psy_table_names != FALSE){
      result_text_psy_condition[pvp] <- if(p_val[pvp] < 0.05){
        t_psy_result_1 <- paste("Группа «",GROUP_1_NAME,"» отличается от группы «",
                            GROUP_2_NAME,"» ",
                            psy_table_names[["Описание со склонением"]][pvp],".", sep = "")
        t_psy_result_2 <- ifelse(mean_group[pvp,1] > mean_group[pvp,2],
                             paste("В группе «",GROUP_1_NAME,
                                   "» выше ",psy_table_names[["Описание"]][pvp],
                                   " по сравнению с группой «",GROUP_2_NAME,"».", sep = ""),
                             paste("В группе «",GROUP_1_NAME,
                                   "» ниже ",psy_table_names[["Описание"]][pvp],
                                   " по сравнению с группой «",GROUP_2_NAME,"».", sep = ""))
        t_psy_result_3 <- ifelse(mean_group[pvp,1] > mean_group[pvp,2],
                             paste("Такой психологический феномен как ",
                                   psy_table_names[["Описание"]][pvp],
                                   " больше в группе «",GROUP_1_NAME,
                                   "», чем в группе «",GROUP_2_NAME,"».", sep = ""),
                             paste("Такой психологический феномен как ",
                                   psy_table_names[["Описание"]][pvp],
                                   " меньше в группе «",GROUP_1_NAME,
                                   "», чем в группе «",GROUP_2_NAME,"».", sep = ""))
        print(text_rand(t_psy_result_1, t_psy_result_2, t_psy_result_3))    
      } else {
        paste("Группа «",GROUP_1_NAME,"» ",psy_table_names[["Описание"]][pvp],
              " не отличается от группы «",GROUP_2_NAME,"»", sep = "")
      } 
    } else {
      result_text_psy_condition[pvp] <- paste("", sep = "")
    }
  }

  result_text_psy_condition <- as.character(result_text_psy_condition)

  ######################Итоговая таблица со всеми данными#######################
  # сохраняю все среднее арифметическое + значение критерия и уровень значимости в отдельный дата фрейм
  all_table <- data.frame(Name = all_table_names[["Названия шкал"]], 
                          Mean_1 = as.numeric(mean_group[,1]), 
                          Mean_2 = as.numeric(mean_group[,2]), 
                          U = as.numeric(statistic), 
                          p_value = as.numeric(p_val), 
                          p_value_star = p_val_star, 
                          stat_condition = result_text_condition, 
                          mean_condition = mean_text_condition,
                          psy_condition = result_text_psy_condition)
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

mww_xlsx <- function(MAIN_DF, GROUP_VAR, GROUP_1_NAME, GROUP_2_NAME){
  #убираю из стат. аналиа данные группы
  MAIN_DF_STAT <- MAIN_DF[,!names(MAIN_DF) == GROUP_VAR]

  #######################Расчет средних#######################
  ###рассчитываю средние значения в каждой группе
  #фильтрую значения переменных по первой группе
  filter_df_group_data_1 <- subset(MAIN_DF, MAIN_DF[GROUP_VAR] == GROUP_1_NAME)

  #удаляю группирующую переменную, чтобы не путалась в итоговом выводе
  filter_df_group_data_1[GROUP_VAR] <- NULL

  #определяю переменную в которую будут писаться значения
  #прохожу циклом по списку переменных и рассчитываю среднее значение попутно записывая его в новую переменную
  #округление до 3 знака после запятой

  mean_group_data_1 <- c()

  for(i in 1:ncol(filter_df_group_data_1))
    mean_group_data_1[i] <- mean(as.numeric(filter_df_group_data_1[[i]]))

  mean_group_data_1 <- round(mean_group_data_1, 3)

  ### расчитываю значения для группы 2
  #фильтрую значения переменных по второй группе
  filter_df_group_data_2 <- subset(MAIN_DF, MAIN_DF[GROUP_VAR] == GROUP_2_NAME)

  #удаляю группирующую переменную, чтобы не путалась в итоговом выводе
  filter_df_group_data_2[GROUP_VAR] <- NULL

  #определяю переменную в которую будут писаться значения
  #прохожу циклом по списку переменных группы 2 и рассчитываю среднее значение попутно записывая его в новую переменную
  #округление до 3 знака после запятой
  mean_group_data_2 <- c()

  for(i in 1:ncol(filter_df_group_data_2))
    mean_group_data_2[i] <- mean(as.numeric(filter_df_group_data_2[[i]]))

  mean_group_data_2 <- round(mean_group_data_2, 3)

  #ввожу переменную для сохранения ТЕКСТОВ результатов вывода по медиане
  # mean_text_condition <- c()

  # for(i in 1:length(mean_group_data_1))
  #   mean_text_condition[i] <- if(mean_group_data_1[i] > mean_group_data_2[i]) {
  #     t_over_1 <- paste("Среднее значение в группе ",GROUP_1_NAME," (X =",mean_group_data_1[i],") больше среднего значения группы ",GROUP_2_NAME," (X =",mean_group_data_2[i],"). ", sep = "")
  #     t_over_2 <- paste("Больше 2", sep = "")
  #     t_over_3 <- paste("Больше 3", sep = "")
  #   } else if (mean_group_data_1[i] < mean_group_data_2[i]) {
  #     t_less_1 <- paste("Среднее значение в группе ",GROUP_1_NAME," (X =",mean_group_data_1[i],") меньше среднего значения группы ",GROUP_2_NAME," (X =",mean_group_data_2[i],"). ", sep = "")
  #     t_less_2 <- paste("Меньше 2", sep = "")
  #     t_less_3 <- paste("Меньше 3", sep = "")
  #   } else {
  #     t_equal_1 <- paste("Среднее значение в группе ",GROUP_1_NAME," (X =",mean_group_data_1[i],") равна среднему значению группы ",GROUP_2_NAME," (X =",mean_group_data_2[i],"). ", sep = "")
  #     t_equal_2 <- paste("Равно 2", sep = "")
  #     t_equal_3 <- paste("Равно 3", sep = "")
  #   }
  #  mean_text_condition <- cbind(mean_text_condition, condition[i])


  #######################Ранжирование данных#######################
  #создаю дата фрейм для ранжирования и удаляю из него группирующую переменную
  main_df_rank <- MAIN_DF
  main_df_rank[GROUP_VAR] <- NULL

  #созданию дата фрейм для сохранения результатов ранжирования
  rank_groups <- data.frame(group = MAIN_DF[[GROUP_VAR]])
  names(rank_groups) <- GROUP_VAR

  #прохожу по каждой шкале и ранжирую значения и пишу все в новый дата фрейм
  for(rg in names(main_df_rank)){
    rank_group_one <- rank(main_df_rank[[rg]])
    rank_groups <- cbind(rank_group_one, rank_groups)
  }


  ###рассчитываю средние ранги значения в каждой группе
  #фильтрую ранги значений переменных по первой группе
  main_df_rank_filter_group_data_1 <- subset(rank_groups, rank_groups[GROUP_VAR] == GROUP_1_NAME)

  #удаляю группирующую переменную, чтобы не путалась в итоговом выводе
  main_df_rank_filter_group_data_1[GROUP_VAR] <- NULL

  #определяю переменную в которую будут писаться значения
  mean_rank_group_data_1 <- c()

  #прохожу циклом по списку переменных и рассчитываю среднее значение попутно записывая его в новую переменную
  for(mrg in names(main_df_rank_filter_group_data_1))
    mean_rank_group_data_1[mrg] <- mean(as.numeric(main_df_rank_filter_group_data_1[[mrg]]))

  #округление до 3 знака после запятой
  mean_rank_group_data_1 <- as.numeric(round(mean_rank_group_data_1, 3))


  #фильтрую ранги значений переменных по второй группе
  main_df_rank_filter_group_data_2 <- subset(rank_groups, rank_groups[GROUP_VAR] == GROUP_2_NAME)

  #удаляю группирующую переменную, чтобы не путалась в итоговом выводе
  main_df_rank_filter_group_data_2[GROUP_VAR] <- NULL

  #определяю переменную в которую будут писаться значения
  mean_rank_group_data_2 <- c()

  #прохожу циклом по списку переменных и рассчитываю среднее значение попутно записывая его в новую переменную
  for(mrg in names(main_df_rank_filter_group_data_2))
    mean_rank_group_data_2[mrg] <- mean(as.numeric(main_df_rank_filter_group_data_2[[mrg]]))

  #округление до 3 знака после запятой
  mean_rank_group_data_2 <- as.numeric(round(mean_rank_group_data_2, 3))

  #свожу данные по рангам в одну таблицу
  rank_group <- data.frame(mean_rank_group_data_1, mean_rank_group_data_2)


  #Функция расчета уровня значимости

  mu_test_p_val <- function(var_name, df_name = MAIN_DF){
    result_manna_uitney_p_val <- c()
    result_manna_uitney_p_val <- wilcox.test(as.numeric(df_name[[var_name]]) ~ df_name[[GROUP_VAR]], 
                                             paired = FALSE, exact = F, correct = F)
    result_manna_uitney_p_val$p.value <- as.numeric(round(result_manna_uitney_p_val$p.value, 3))
  }

  #Функция расчета статистики
  mu_test_statistic <- function(var_name, df_name = MAIN_DF){
    result_manna_uitney_p_val <- c()
    result_manna_uitney_p_val <- wilcox.test(as.numeric(df_name[[var_name]]) ~ df_name[[GROUP_VAR]], 
                                             paired = FALSE, exact = F, correct = F)
    result_manna_uitney_p_val$statistic <- as.numeric(round(result_manna_uitney_p_val$statistic, 3))
  }


  statistic <- c()
  for(s in names(MAIN_DF_STAT))
    statistic[s] <- mu_test_statistic(s)
  statistic <- as.numeric(statistic)

  p_val <- c()
  for(p in names(MAIN_DF_STAT))
    p_val[p] <- as.numeric(mu_test_p_val(p))

  p_val <- as.numeric(p_val)


  #######################Итоговая таблица со всеми данными#######################
  # сохраняю все среднее арифметическое + значение критерия и уровень значимости в отдельный дата фрейм
  all_table <- data.frame(
      Name = names(filter_df_group_data_1),
      Mean_1 = mean_group_data_1, 
      Mean_2 = mean_group_data_2,
      Rank_1 = rank_group$mean_rank_group_data_1, 
      Rank_2 = rank_group$mean_rank_group_data_2,
      U = statistic, 
      p_value = p_val
      # condition = mean_text_condition
  )

  return(all_table)
}

mww_graph <- function(all_table, MAIN_DF, GROUP_VAR, GROUP_1_NAME, GROUP_2_NAME) {
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
                  cex.lab=0.7,
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

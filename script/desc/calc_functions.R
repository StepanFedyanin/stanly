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

  df <- as.data.frame(groups)

  return(df)
}

get_descriptive <- function(MAIN_DF) {
  #получаю названия шкал
  MAIN_DF_SCALE_NAMES <- names(MAIN_DF)

  #провожу все расчеты и убираю лишние данные
  descriptive <- describe(MAIN_DF, na.rm = TRUE, check=FALSE)
  descriptive <- descriptive[c(-1,-2,-6,-7,-10,-13)]
  descriptive <- descriptive[c(1,2,3,6,7,4,5)]
  descriptive <- round(descriptive,3)
  descriptive[is.na(descriptive)] <- 0  

  rownames(descriptive) <- MAIN_DF_SCALE_NAMES
  colnames(descriptive) <- c("Среднее арифметическое", 
                             "Стандартное отклонение", 
                             "Медиана",
                             "Асимметрия", 
                             "Эксцесс",
                             "Минимум", 
                             "Максимум")
  return(descriptive)
}

calc_desc <- function(MAIN_DF_SCALE_NAMES, descriptive) {

  ## Текстовые вводы с графиками
  mean_text_condition <- NULL
  sd_text_condition <- NULL
  median_text_condition <- NULL
  skew_text_condition <- NULL
  kurtosis_text_condition <- NULL
  min_text_condition <- NULL
  max_text_condition <- NULL

  for(i in 1:length(MAIN_DF_SCALE_NAMES)){
    mean_text_condition[i] <- if(1 == 1){
      t_over_1 <- paste("Среднее значение по шкале «",MAIN_DF_SCALE_NAMES[i],"» составляет ",descriptive[i,1],". ", sep = "")
      t_over_2 <- paste("По шкале «",MAIN_DF_SCALE_NAMES[i],"» среднее значение составляет ",descriptive[i,1],". ", sep = "")
      t_over_3 <- paste("Рассчитан следующий средний показатель по шкале «",MAIN_DF_SCALE_NAMES[i],"» его значение ",descriptive[i,1],". ", sep = "")
      text_rand(t_over_1, t_over_2, t_over_3)
    }
    
    sd_text_condition[i] <- if(descriptive[1,2] > descriptive[i,1]){
      paste("По данной шкале имеется сильный разброс значений относительного среднего (сигма=",descriptive[i,2],"). Это говорит о том, что признак сильно варьируется по данной выборке. ", sep = "")
        } else if(descriptive[i,2] < descriptive[i,1]/4){
      paste("По данной шкале имеется слабый разброс значений относительного среднего (сигма=",descriptive[i,2],"). Это говорит о том, что признак очень мало варьируется по данной выборке. ", sep = "")
        } else {
      paste("Разброс значений по выборке в пределах нормы (сигма=",descriptive[i,2],"). ", sep = "")  
        }
    
    median_text_condition[i] <- if(1 == 1){
      t_over_1 <- paste("Медиана выборки равна ",descriptive[i,3],". ", sep = "")
      t_over_2 <- paste("Медианное значение составляет ",descriptive[i,3],". ", sep = "")
      t_over_3 <- paste("Значение медианы по данной шкале равно  ",descriptive[i,3],". ", sep = "")
      text_rand(t_over_1, t_over_2, t_over_3)
    }
    
    skew_text_condition[i] <- if(descriptive[i,4] < -0.3){
      paste("Выявлена правосторонняя асимметрия (A=",descriptive[i,4],") - в выборке чаще встречаются значения выше среднего. ", sep = "")
        } else if(descriptive[i,4] > 0.3){
      paste("Выявлена левосторонняя асимметрия (A=",descriptive[i,4],") - в выборке чаще встречаются значения ниже среднего. ", sep = "")
        } else {
      paste("Высокие, средние и низкие значения в выборке распределены очень близко к нормальному распределению (А=",descriptive[i,4],"). ", sep = "")          
        }

      kurtosis_text_condition[i] <- if(descriptive[i,5] > 0.5){
      paste("Выявлен положительный эксцесс (Е=",descriptive[i,5],"). В выборке значения находятся преимущественного около среднего арифметического. ", sep = "")
        } else if(descriptive[i,5] < -0.5){
      paste("Выявлен отрицательный эксцесс (Е=",descriptive[i,5],"). В выборке много значений находятся около крайних значений минимума и максимума. ", sep = "")
        } else {
      paste("Значения в выборке относительно среднего распределены нормально (Е=",descriptive[i,5],"). ", sep = "")  
        }
      
    min_text_condition[i] <- if(1 == 1){
      t_over_1 <- paste("Значение минимума равно ",descriptive[i,6],", ", sep = "")
      t_over_2 <- paste("Минимум составляет ",descriptive[i,6],", ", sep = "")
      t_over_3 <- paste("Минимум равен ",descriptive[i,6],", ", sep = "")
      text_rand(t_over_1, t_over_2, t_over_3)
    }
    
    max_text_condition[i] <- if(1 == 1){
      t_over_1 <- paste("значение максимума равно ",descriptive[i,7],". ", sep = "")
      t_over_2 <- paste("максимум составляет ",descriptive[i,7],". ", sep = "")
      t_over_3 <- paste("максимум равен ",descriptive[i,7],". ", sep = "")
      text_rand(t_over_1, t_over_2, t_over_3)
    }
    
    cat(mean_text_condition[i],
        sd_text_condition[i],
        median_text_condition[i],
        skew_text_condition[i],
        kurtosis_text_condition[i],
        min_text_condition[i],
        max_text_condition[i], sep = "")
    cat("\n", sep="\n")
  }
}

calc_xlsx_main <- function(MAIN_DF, xlsx_file) {
  # В эксель файл вывести таблицу с расчитываемыми показателями - среднее арифметическое, мода, медиана, асимметрия, эксцесс
  MAIN_DF_SCALE_NAMES <- names(MAIN_DF[,1:ncol(MAIN_DF)])
  descriptive <- get_descriptive(MAIN_DF)

  write.xlsx(as.data.frame(MAIN_DF, optional = TRUE), file=xlsx_file, col.names=TRUE, row.names=FALSE, sheetName='Входные данные')
  write.xlsx(as.data.frame(descriptive, optional = TRUE), file=xlsx_file, col.names=TRUE, row.names=FALSE, append=TRUE, sheetName='Результат')
}
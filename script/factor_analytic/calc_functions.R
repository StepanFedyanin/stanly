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

calc_xlsx_main <- function(MAIN_DF, xlsx_file) {

  MAIN_DF_NAMES <- names(MAIN_DF)
  # устанавливаю значение критерия кайзера, по умолчанию рано 1
  KAISER_CRITERIA <- 1

  # определяю количество факторов в анализе
  # считаю факторный анализ и считаю количество факторов больше критерия кайзера
  prefit <- principal(MAIN_DF, rotate="varimax")
  NUMBER_OF_FACTOR <- length(prefit$values[prefit$values > KAISER_CRITERIA])

  #######################БЛОК С ОСНОВНЫМИ РАСЧЕТАМи#######################
  # считаю нужную модель
  fit <- principal(MAIN_DF, nfactors=NUMBER_OF_FACTOR, rotate="varimax")

  # считаю значения КМО
  KMO <- KMO(MAIN_DF)
  if(is.nan(KMO$MSA) == T){
    fit_KMO <- 0
  } else {
    fit_KMO <- KMO$MSA
  }

  table_fit_KMO <- data.frame(round(fit_KMO,3))
  row.names(table_fit_KMO) <- "Показатель КМО"
  colnames(table_fit_KMO) <- NULL


  # считаю собственные значения, процент объясненной дисперсии и процент накопленной дисперсии
  fit_values <- as.vector(round(fit$values[fit$values > KAISER_CRITERIA],3))
  fit_prop_var <- as.vector(round(fit$Vaccounted[2:2, 1:NUMBER_OF_FACTOR],5) * 100)
  fit_cum_var <- as.vector(round(fit$Vaccounted[3:3, 1:NUMBER_OF_FACTOR],5) * 100)
  fit_factor_num <- c(1:NUMBER_OF_FACTOR)
  fit_total_variance <- t(rbind(fit_factor_num, fit_values, fit_prop_var, fit_cum_var))

  fit_total_variance <- data.frame(fit_total_variance)
  row.names(fit_total_variance) <- NULL
  colnames(fit_total_variance) <- c("Фактор", "Начальные собственные значения", "% дисперсии", "Кумулятивный %")

  # считаю матрицу с факторными нагрузками
  fit_loadings <- data.frame(round(fit$loadings[1:length(MAIN_DF_NAMES), 1:NUMBER_OF_FACTOR],3))
  fit_loadings_colnames <- NULL

  # звездочкой отражаю принадлежность значения к фактору 
  fit_loadings_star <- matrix(NA, nrow = length(MAIN_DF_NAMES), ncol = NUMBER_OF_FACTOR)
  fit_loadings_scale_name <- matrix(NA, nrow = length(MAIN_DF_NAMES), ncol = NUMBER_OF_FACTOR)
  for(m in 1:length(MAIN_DF_NAMES)){
    for(n in 1:NUMBER_OF_FACTOR){
      if(abs(fit_loadings[[m,n]]) == max(abs(fit_loadings[m,]))){
        result_abs <- paste(fit_loadings[[m,n]],"*", 
                            sep = "")
        fit_loadings_star[[m,n]] <- result_abs
        result_scale_name <- paste("«",MAIN_DF_NAMES[[m]],"»(",fit_loadings[[m,n]],")", 
                            sep = "")
        fit_loadings_scale_name[[m,n]] <- result_scale_name
      } else {
        result_abs <- paste(fit_loadings[[m,n]], 
                            sep = "")
        fit_loadings_star[[m,n]] <- result_abs
        result_scale_name <- paste(NA, 
                            sep = "")
        fit_loadings_scale_name[[m,n]] <- result_scale_name
      }
    }
  }
  fit_loadings_star <- data.frame(fit_loadings_star)
  fit_loadings_scale_name <- data.frame(fit_loadings_scale_name)

  # определяю названия факторов
  for(i in 1:NUMBER_OF_FACTOR){
    column_name <- as.character(paste("Фактор ",i))
    fit_loadings_colnames <- rbind(fit_loadings_colnames, column_name)
  }
  names(fit_loadings_star) <- fit_loadings_colnames
  row.names(fit_loadings_star) <- row.names(fit_loadings)

  factor_list <- c("Первый фактор состоит из следующих шкал: ", 
                   "Второй фактор состоит из следующих шкал: ", 
                   "Третий фактор состоит из следующих шкал: ", 
                   "Четвертый фактор состоит из следующих шкал: ", 
                   "Пятый фактор состоит из следующих шкал: ",
                   "Шестой фактор состоит из следующих шкал: ",
                   "Седьмой фактор состоит из следующих шкал: ",
                   "Восьмой фактор состоит из следующих шкал: ",
                   "Девятый фактор состоит из следующих шкал: ",
                   "Десятый фактор состоит из следующих шкал: ",
                   "Одинадцатый фактор состоит из следующих шкал: ",
                   "Двенадцатый фактор состоит из следующих шкал: ",
                   "Тринадцатый фактор состоит из следующих шкал: ",
                   "Четырнадцатый фактор состоит из следующих шкал: ",
                   "Пятнадцатый фактор состоит из следующих шкал: ",
                   "Шестнадцатый фактор состоит из следующих шкал: ",
                   "Семнадцатый фактор состоит из следующих шкал: ",
                   "Восемнадцатый фактор состоит из следующих шкал: ",
                   "Десятнадцатый фактор состоит из следующих шкал: ",
                   "Двадцатый фактор состоит из следующих шкал: ",
                   "Двадцать первый фактор состоит из следующих шкал: ",
                   "Двадцать второй фактор состоит из следующих шкал: ",
                   "Двадцать третий фактор состоит из следующих шкал: ",
                   "Двадцать четвертый фактор состоит из следующих шкал: ",
                   "Двадцать пятый фактор состоит из следующих шкал: ",
                   "Двадцать шестой фактор состоит из следующих шкал: ",
                   "Двадцать седьмой фактор состоит из следующих шкал: ",
                   "Двадцать восьмой фактор состоит из следующих шкал: ",
                   "Двадцать девятый фактор состоит из следующих шкал: ",
                   "Тридцатый фактор состоит из следующих шкал: ")

  factor_text <- NULL
  for(z in 1:NUMBER_OF_FACTOR){
    factor_text_one <- gsub("NA, |, NA","", paste(fit_loadings_scale_name[[z]], collapse = ", "))
    factor_text_one <- paste(factor_list[[z]],factor_text_one,".", sep="")
    factor_text <- rbind(factor_text, factor_text_one)
  }

  write.xlsx(as.data.frame(MAIN_DF, optional = TRUE), file=xlsx_file, col.names=TRUE, row.names=FALSE, sheetName='Входные данные')
  write.xlsx(as.data.frame(fit_loadings_star, optional = TRUE), file=xlsx_file, col.names=TRUE, row.names=TRUE, append=TRUE, sheetName='Результат')
}

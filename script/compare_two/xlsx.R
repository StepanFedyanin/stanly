setwd('./script/compare_two/')

if(!exists("include_libraries", mode="function")) source("../functions.R")
if(!exists("st", mode="function")) source("../st.R")

args <- commandArgs(TRUE)
json_file <- args[1]
xlsx_file <- args[2]
with_mean <- args[3]

include_libraries()

# for test 
# data <- rjson::fromJSON('{"group_name_1":"g1","group_count_1":4,"group_data_1":{"Шаг 2":{"1":0,"2":0,"3":0,"4":0},"Шаг 3":{"1":0,"2":0,"3":0,"4":0},"Шаг 4":{"1":0,"2":0,"3":0,"4":0}},"group_name_2":"g2","group_count_2":6,"group_data_2":{"Шаг 2":{"1":0,"2":0,"3":0,"4":0,"5":0,"6":0},"Шаг 3":{"1":0,"2":0,"3":0,"4":0,"5":0,"6":0},"Шаг 4":{"1":0,"2":0,"3":0,"4":0,"5":0,"6":0}}}')

data <- rjson::fromJSON(file=json_file)

group_var <- get_group_var('Группа', data$group_name_1, data$group_name_2)
GROUP_VAR <- group_var["name"]
GROUP_1_NAME <- group_var["g_name_1"]
GROUP_2_NAME <- group_var["g_name_2"]

#зависимые выборки?
#если FALSE / F то считает НЕЗАВИСИМЫЕ ВЫБОРКИ, иначе зависимые
pair <- T
stat_name <- ifelse(pair == TRUE, "Т-Стьюдента для зависимых выборок", "Т-Стьюдента для независимых выборок")

json_res <- function(MAIN_DF) {
  all_table <- st_xlsx(MAIN_DF, GROUP_VAR, GROUP_1_NAME, GROUP_2_NAME, pair)

  boxplot_names <- c(GROUP_1_NAME, GROUP_2_NAME)
  all_table$Name <- as.character(all_table$Name)
  all_table$condition <- as.character(all_table$condition)
  res <- list()

  if (with_mean == 'full') {
    res <- all_table
  } else {
    U <- c()
    p_value <- c()

    for (i in 0:length(all_table$U))
        U[i] <- all_table$U[i]

    for (i in 0:length(all_table$p_value))
        p_value[i] <- all_table$p_value[i]

    res[['U']] <- U
    res[['p_value']] <- p_value
  }

  write.xlsx(as.list(MAIN_DF), file=xlsx_file, col.names=TRUE, row.names=FALSE, sheetName='Входные данные')
  write.xlsx(res, file=xlsx_file, col.names=TRUE, row.names=FALSE, append=TRUE, sheetName='Результат')
}

main_tibble <- prepare_data_of_two(data, GROUP_VAR)
json_res(main_tibble)

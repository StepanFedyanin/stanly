setwd('./script/mann_whitney/')

if(!exists("include_libraries", mode="function")) source("../functions.R")
if(!exists("mww", mode="function")) source("../mww.R")

include_libraries()

args <- commandArgs(TRUE)
json_file <- args[1]
xlsx_file <- args[2]
with_mean <- args[3]

# for test 
# data <- rjson::fromJSON('{"group_name_1":"1","group_name_2":"2","group_count_1":"1","group_count_2":"2","group_data_1":{"шкала":{"1":1},"Шкала 2":{"1":1},"Шкала 3":{"1":1}},"group_data_2":{"шкала":{"1":1,"2":1},"Шкала 2":{"1":1,"2":1},"Шкала 3":{"1":1,"2":1}}}')

data <- rjson::fromJSON(file=json_file)

group_var <- get_group_var('Группа', data$group_name_1, data$group_name_2)
GROUP_VAR <- group_var["name"]
GROUP_1_NAME <- group_var["g_name_1"]
GROUP_2_NAME <- group_var["g_name_2"]

json_res <- function(MAIN_DF) {

  all_table <- mww_xlsx(MAIN_DF, GROUP_VAR, GROUP_1_NAME, GROUP_2_NAME)
  boxplot_names <- c(GROUP_1_NAME, GROUP_2_NAME)
  res <- list()
  all_table$Name <- as.character(all_table$Name)

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

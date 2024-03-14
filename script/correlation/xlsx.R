setwd('./script/correlation/')

if(!exists("include_libraries", mode="function")) source("../functions.R")
if(!exists("calc_prepare_data", mode="function")) source("calc_functions.R")

include_libraries()

args <- commandArgs(TRUE)

json_file = args[1]
xlsx_file = args[2]
# with_mean = args[3] # средние значения
calc_name = args[4]

data <- rjson::fromJSON(file = json_file)

# for test 
# data <- rjson::fromJSON('{"group_name_1":"g1","group_count_1":4,"group_data_1":{"Шкала 1":{"1":65,"2":65,"3":6565,"4":8},"scale 1 ":{"1":65,"2":65,"3":65,"4":8}}}')

GROUP_VAR <- 'Группа'

METHOD_NAME <- if (calc_name == 'correlation_spearman'){
  'spearman'
} else if (calc_name == 'correlation_pearson') {
  'pearson'
} else {
  'kendall'
}

main_tibble <- calc_prepare_data(data, GROUP_VAR)
calc_xlsx_main(main_tibble, xlsx_file, METHOD_NAME)

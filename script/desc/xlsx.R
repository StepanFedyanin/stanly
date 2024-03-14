setwd('./script/desc/')

if(!exists("include_libraries", mode="function")) source("../functions.R")
if(!exists("calc_prepare_data", mode="function")) source("calc_functions.R")

include_libraries()

args <- commandArgs(TRUE)

json_file = args[1]
xlsx_file = args[2]

data <- rjson::fromJSON(file = json_file)

# GROUP_VAR <- 'Группа'

MAIN_DF <- calc_prepare_data(data, GROUP_VAR)
calc_xlsx_main(MAIN_DF, xlsx_file)

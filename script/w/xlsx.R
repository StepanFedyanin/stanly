setwd('./script/w/')

if(!exists("include_libraries", mode="function")) source("../functions.R")
if(!exists("calc_prepare_data", mode="function")) source("../w_z.R")
if(0) source("calc_functions.R")

include_libraries()

args <- commandArgs(TRUE)

json_file = args[1]
xlsx_file = args[2]

data <- rjson::fromJSON(file = json_file)
GROUP_VAR <- 'Группа'

METHOD_NAME <- "w"
# METHOD_NAME <- "z"

main_tibble <- calc_prepare_data(data, GROUP_VAR)
calc_xlsx_main(main_tibble, xlsx_file, METHOD_NAME)

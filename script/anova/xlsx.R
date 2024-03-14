setwd('./script/anova/')


if(!exists("include_libraries", mode="function")) source("../functions.R")
if(!exists("calc_prepare_data", mode="function")) source("calc_functions.R")

include_libraries()

args <- commandArgs(TRUE)
json_file <- args[1]
xlsx_file <- args[2]

data <- rjson::fromJSON(file = json_file)

MAIN_DF <- calc_prepare_data(data)
all_data <- calc_anova(MAIN_DF)

write.xlsx(all_data, file = xlsx_file)

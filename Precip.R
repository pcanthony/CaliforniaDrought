allMonthlyPrecipData <- function() {
	myfiles <- (Sys.glob("*.csv"))

	allData <<- data.frame(station = character(0), sensor = numeric(0), year = numeric(0), month = numeric(0), Jan = numeric(0), Feb = numeric(0), Mar = numeric(0), Apr = numeric(0), May = numeric(0), Jun = numeric(0), Jul = numeric(0), Aug = numeric(0), Sep = numeric(0), Oct = numeric(0), Nov = numeric(0), Dec = numeric(0))
	
	for (i in myfiles) {
		tempData <- read.table(i, sep = ",", skip = 3, col.names = names(allData), na.strings = "m", fill = TRUE, header = TRUE, stringsAsFactors = FALSE)
		tempData <- tempData[!is.na(tempData$year),]
		allData <<- rbind(allData, tempData)
	}

	allData$sensor <<- NULL #remove empty columns
	allData$month <<- NULL
	allData <<- allData[(rowSums(is.na(allData)) <= 6), ] #remove lines that have >6 NA's
	allData$Total <<- rowSums(allData[, -c(1:2)], na.rm = TRUE)
	write.csv(allData, file = "../allData.csv", row.names = FALSE)	
}
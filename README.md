###Introduction
The Precip.py script generates a Google map of precipitation levels measured at weather stations in California between January 1990 and September 2014. The map shows an icon for each station with the number of inches of precipitation measured at that station during an input time period.  Each station's icon is colored based on a comparison of the station's precipitation level with other stations' for the same time period, or alternatively with the same station's levels for other available time periods.  The latter coloring scheme is accessed using the "--history" flag.

All data were obtained from the California Department of Water Resources Data Exchange Center (http://cdec.water.ca.gov/index.html).

###Files
The following files and directories must be present in the same working directory as Precip.py to run the script:

* allData.csv (a tidy data set of precipitation data for all stations.  Can be generated by running the Precip.R script on data in the /weather data directory.)
* CA stations with accum monthly precip.html.  This page contains latitudes and longitudes of the weather stations.
* Directories containing icons to plot on the map: /map_numbers_black, /map_numbers_blue, /map_numbers_red, /map_numbers_orange, /map_numbers_green

###Input Format
$./Precip.py [--history] [year(YYYY)] [month(MM)]

###Examples

####$./Precip.py 2013 01
Plots precipitation levels for January 2013.  Data for this month are compared among stations and a Z-score is calculated for each station.  Stations with Z-scores of > +1 (i.e., stations that received more precipitation than the average station during January 2013) are colored blue. Stations with Z-scores of < -1 (i.e., stations that received less precipitation than the average station during January 2013) are colored red.  All other stations are colored black.

####$./Precip.py 2013
Plots accumulated precipitation levels for the entire year of 2013.  Data for this year are compared among stations and a Z-score is calculated for each station.  Stations with Z-scores of > +1 (i.e., stations that received more precipitation than the average station during 2013) are colored blue. Stations with Z-scores of < -1 (i.e., stations that received less precipitation than the average station during 2013) are colored red.  All other stations are colored black.

####$./Precip.py --history 2013 01
Plots precipitation levels for January 2013.  Data for each station for this month are compared with data for the same station obtained in January of all other available years.
For each station, a Z-score of the January 2013 precipitation level is calculated relative to other January levels.  Stations with Z-scores of > +1 (i.e., stations that received more precipitation during January 2013 than during the average January) are colored green. Stations with Z-scores of < -1 (i.e., stations that received less precipitation during January 2013 than during the average January) are colored orange.  All other stations are colored black.

####$./Precip.py --history 2013
Plots accumulated precipitation levels for the year 2013.  Data for each station for this year are compared with data for the same station obtained in all other available years.
For each station, a Z-score of the 2013 precipitation level is calculated relative to levels for other years.  Stations with Z-scores of > +1 (i.e., stations that received more precipitation during 2013 than during the average year) are colored green. Stations with Z-scores of < -1 (i.e., stations that received less precipitation during 2013 than during the average year) are colored orange.  All other stations are colored black.

####$./Precip.py 01
Plots the precipitation level for each station in January, averaged over all available years.  Data are compared among stations and a Z-score is calculated for each station.  Stations with Z-scores of > +1 (i.e., stations that receive more precipitation than the average station during January) are colored blue. Stations with Z-scores of < -1 (i.e., stations that receive less precipitation than the average station during January) are colored red.  All other stations are colored black.

####$./Precip.py
Plots the yearly accumulated precipitation level for each station, averaged over all available years.  Data are compared among stations and a Z-score is calculated for each station.  Stations with Z-scores of > +1 (i.e., stations that receive more precipitation than the average station) are colored blue. Stations with Z-scores of < -1 (i.e., stations that receive less precipitation than the average station) are colored red.  All other stations are colored black.
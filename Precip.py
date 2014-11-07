#!/usr/bin/python

from __future__ import print_function
import sys
import re
from numpy import mean
from numpy import std


def ReadStationList(filename):
    """
    Parses an HTML file containing a table of weather stations with their GPS coordinates.
    Returns a list of tuples, each containing the name, longitude, and latitude of a station.
    """
    
    f = open(filename, 'rU')
    myTable = f.read()
    f.close()

    myStations = re.findall('staMeta\?station_id=(\w\w\w)\">\w\w\w</a></td><td>[\w\s\(\)-]+</td><td>[\w\s\(\)-]+</td><td>[\w\s\(\)-]+</td><td>([\d.-]+)</td><td>([\d.]+)</td>', myTable)
    #make tuples of stations: station name, longitude, latitude

    return myStations


def PrecipDataMeanStdM(data, month):
    """
    Takes the tidy precipitation dataset and, for each line, reads the precipitation for the input month.
    Builds a list of non-NA precipitation values for each station, in the input month across all available years.
    Returns two dictionaries, each with station names as the keys.
    The MeanData and StdData dictionaries have the mean and standard deviation, respectively, of precipitation for each station as the values.
    """

    MeanData = {} #Start a dictionary.
    StdData = {}

    oldStation = None
    stationPrecip = []
    for i in data:
        line = i.split(',')
        try:
            monthPrecip = float(line[month + 1])        
            thisStation = line[0].strip('"')
            if not oldStation or thisStation == oldStation:
                stationPrecip.append(monthPrecip)
            else:
                MeanData[oldStation] = mean(stationPrecip)
                StdData[oldStation] = std(stationPrecip)
                stationPrecip = [monthPrecip]
            oldStation = thisStation
        except ValueError:
            pass

    if oldStation not in MeanData.keys(): #Dictionary values for the last station in the dataset.
        MeanData[oldStation] = mean(stationPrecip)
        StdData[oldStation] = std(stationPrecip)

    return MeanData, StdData


def PrecipDataMeanStdY(data):
    """
    Takes the tidy precipitation dataset and, for each line, reads the total precipitation for each year.
    Builds a list of non-NA precipitation values for each station, across all available years.
    Returns two dictionaries, each with station names as the keys.
    The MeanData and StdData dictionaries have the mean and standard deviation, respectively, of total precipitation for each station as the values.
    """

    MeanData = {} #Start a dictionary.
    StdData = {}

    oldStation = None
    stationPrecip = []
    for i in data:
        line = i.split(',')
        try:
            yearPrecip = float(line[-1])
            thisStation = line[0].strip('"')
            if not oldStation or thisStation == oldStation:
                stationPrecip.append(yearPrecip)
            else:
                MeanData[oldStation] = mean(stationPrecip)
                StdData[oldStation] = std(stationPrecip)
                stationPrecip = [yearPrecip]
            oldStation = thisStation
        except ValueError:
            pass

    if oldStation not in MeanData.keys(): #Dictionary values for the last station in the dataset.
        MeanData[oldStation] = mean(stationPrecip)
        StdData[oldStation] = std(stationPrecip)

    return MeanData, StdData


def ReadPrecipDataYM(data, year, month):
    """
    Takes the tidy precipitation dataset and reads each line.
    If the year matches the input value, then the precipitation for the input month is read.
    A dictionary is returned with station names as the keys and precipitation for the input month as the values.
    """
    
    myData = {} 
    for i in data:
        line = i.split(',')
        if line[1] == year:
            if "NA" not in line[month + 1]: #line[1] is the year (YYYY). line[month + 1] is the precipitation in a month (e.g., precip. for January is line[2]).
                myData[line[0].strip('"')] = float(line[month + 1])
    return myData

  
def ReadPrecipDataY(data, year):
    """
    Takes the tidy precipitation dataset and reads each line.
    If the year matches the input value, then the total precipitation for the year is read.
    A dictionary is returned with station names as the keys and total precipitation for the input year as the values.
    """

    myData = {} #Start a dictionary.  The keys will be station names and the values will be the amounts of precipitation (in inches) for the specified year.
    for i in data:
        line = i.split(',')
        if line[1] == year:
            if "NA" not in line[-1]: #line[1] is the year (YYYY). line[-1] is the total precipitation for a year.
                myData[line[0].strip('"')] = float(line[-1])
    return myData


class Map(object):
    """
    Wrapper code for Google Maps API.
    Puts a marker on the map at the input coordinates, with the input icon file and mouse-over text.
    """
    
    def __init__(self):
        self._points = []
    def add_point(self, coordinates):
        self._points.append(coordinates)
    def __str__(self):
        centerLat = sum(( x[0] for x in self._points )) / len(self._points)
        centerLon = sum(( x[1] for x in self._points )) / len(self._points)
        markersCode = "\n".join(
            [ """new google.maps.Marker({{
                position: new google.maps.LatLng({lat}, {lon}),
                map: map,
                icon: './map_numbers_{col}/number_{num}.png',
                title: "{name}"
                }});""".format(lat = x[0], lon = x[1], col = x[2], num = int(x[3]), name = x[4]) for x in self._points
            ])
        return """
            <script src="https://maps.googleapis.com/maps/api/js?v=3.exp&sensor=false"></script>
            <div id="map-canvas" style="height: 100%; width: 100%"></div>
            <script type="text/javascript">
                var map;
                function show_map() {{
                    map = new google.maps.Map(document.getElementById("map-canvas"), {{
                        zoom: 6,
                        center: new google.maps.LatLng({centerLat}, {centerLon})
                    }});
                    {markersCode}
                }}
                google.maps.event.addDomListener(window, 'load', show_map);
            </script>
        """.format(centerLat=centerLat, centerLon=centerLon,
                   markersCode=markersCode)


if __name__ == "__main__":

        args = sys.argv[1:]

        if len(args) > 3:
            print('usage: [--history] [year(YYYY)] [month(MM)]')
            sys.exit(1)

        myFile = [] #Read in the tidy data set and store as myFile, which is a list.  Each element of the list is a line of the file.
        f = open('allData.csv', 'rU')
        myFile = f.readlines()
        f.close()

        if len(args) == 0:
            CAprecip = PrecipDataMeanStdY(myFile)[0] #Here CAprecip is station:mean(total precip) dictionary. 
        elif len(args) == 1 and args[0] in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']:
            myMonth = int(args[0])
            CAprecip = PrecipDataMeanStdM(myFile, myMonth)[0]
        elif args[0] == "--history": #Color map by whether precipitation at each station is high or low compared with historical values.
            if len(args) == 3: #Plot precipitation in a single month.
                myYear = args[1]
                myMonth = int(args[2])
                CAprecip = ReadPrecipDataYM(myFile, myYear, myMonth) #Station:precip dictionary for input month of input year
                CAmean, CAstd = PrecipDataMeanStdM(myFile, myMonth) #Station:mean(precip) and station:std(precip) dictionaries for input month in all years.
            elif len(args) == 2: #Plot total precipitation for a year.
                myYear = args[1]
                CAprecip = ReadPrecipDataY(myFile, myYear) #Station:(total precip) dictionary for input year
                CAmean, CAstd = PrecipDataMeanStdY(myFile) #Station:mean(total precip) and station:std(total precip) dictionaries for all years.
        else: #Color map by whether precipitation at each station is high or low compared with other stations in same time period.
            if len(args) == 2: #Plot precipitation in a single month.
                myYear = args[0]
                myMonth = int(args[1])
                CAprecip = ReadPrecipDataYM(myFile, myYear, myMonth) #Station:precip dictionary for input month of input year.
            elif len(args) == 1: #Plot total precipitation for a year.
                myYear = args[0]
                CAprecip = ReadPrecipDataY(myFile, myYear) #Station:(total precip) dictionary for input year

        meanPrecip = mean(CAprecip.values()) #Mean of precipitation values for all stations during input month or year.
        stdPrecip = std(CAprecip.values()) #Standard deviation of precipitation values for all stations during input month or year.

        map = Map()
        CAstations = ReadStationList("CA stations with accum monthly precip.html")

        for i in CAstations:
            thisStation = i[0]
            thisLat = float(i[2])
            thisLong = float(i[1])
            color = None
            if thisStation in CAprecip.keys(): #if the station is in the dictionary of those stations that had data for the requested month or year...
                thisPrecip = CAprecip[thisStation]
                if 'CAmean' in locals(): #Coloring if historical dictionaries have been prepared. 
                    if thisPrecip > CAmean[thisStation] + CAstd[thisStation]:
                        color = 'green'
                    elif thisPrecip < CAmean[thisStation] - CAstd[thisStation]:
                        color = 'orange'
                elif thisPrecip > meanPrecip + stdPrecip: #Coloring if historical dictionaries have not been prepared.
                    color = 'blue'
                elif thisPrecip < meanPrecip - stdPrecip:
                    color = 'red'
                if not color:
                    color = 'black'
                if thisPrecip >= 101:
                    plot_number = 101
                else:
                    plot_number = int(round(thisPrecip))
                map.add_point((thisLat, thisLong, color, plot_number, thisStation)) #...plot a point on the map at the correct latitude and longitude,
                              #with the plotted number representing the amount of precipitation recorded at the station in the requested month/year (rounded to the nearest integer).
        with open("output.html", "w") as out:
            print(map, file=out)
        print("Map generated.  Please load output.html in your browser or hit refresh.")

#!/bin/python3

from tempByMonth import getHighsLowsOfMonth, getHighsLowsOfMonthById

#locId = "CITY:US000001" # Washington D.C.
locId = "CITY:VE000008" # Maracaibo, Venezuela

#city = "Denver"
#state = "CO"

city = "Honolulu"
state = "HI"

year = 2005
avgTempRangeSum = 0
for month in range(1, 13):
    highs, lows = getHighsLowsOfMonth(month, year, city, state)
    #highs, lows = getHighsLowsOfMonthById(month, year, locId) #uncomment to use city IDs instead

    tempRangeSum = 0
    minTempRange = 100
    maxTempRange = 0
    for i in range(0, len(highs)):

        tempRangeSum += abs(highs[i] - lows[i])
        
        if (abs(highs[i] - lows[i]) > maxTempRange):
            maxTempRange = abs(highs[i] - lows[i])

        if (abs(highs[i] - lows[i]) < minTempRange):
            minTempRange = abs(highs[i] - lows[i])

    avgTempRange = tempRangeSum / len(highs)
    avgTempRangeSum += avgTempRange

    print("Month:%s Min:%.1f Avg:%.1f Max:%.1f" % (str(month).zfill(2), minTempRange, avgTempRange, maxTempRange))

print("Average Temperature Change in a Year: %.1f degrees fahrenheit" % (avgTempRangeSum/12.0))


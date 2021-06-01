import ctypes
import os
from datetime import timedelta, date
from time import sleep, localtime, timezone, altzone
import math
from astral import Astral
#from threading import Thread

def splitDayIntoParts(n: int) -> list[timedelta]:
    sunrise, sunset = calculateDaytime(latitude, longitude)

    midnightToSunrise = []
    numberOfNightPictures = math.ceil(n / 4)
    secsFromMidnightToSunrise = sunrise - timedelta(seconds=0)
    secsFromMidnightToSunrise = secsFromMidnightToSunrise.total_seconds()
    interval = secsFromMidnightToSunrise / numberOfNightPictures
    for i in range(1, numberOfNightPictures):
        midnightToSunrise.append(timedelta(seconds=i*interval))
    midnightToSunrise.append(sunrise)

    sunriseToSunset = []
    numberOfDayPictures = math.floor(n / 2)
    secsFromSunriseToSunset = sunset - sunrise
    secsFromSunriseToSunset = secsFromSunriseToSunset.total_seconds()
    interval = secsFromSunriseToSunset / numberOfDayPictures
    for i in range(1, numberOfDayPictures):
        sunriseToSunset.append(sunrise + timedelta(seconds=i*interval))
    sunriseToSunset.append(sunset)

    sunsetToMidnight = []
    numberOfNightPictures = math.floor(n / 4)
    secsFromSunsetToMidnight = timedelta(days=1) - sunset
    secsFromSunsetToMidnight = secsFromSunsetToMidnight.total_seconds()
    interval = secsFromSunsetToMidnight/numberOfNightPictures
    for i in range(1, numberOfNightPictures):
        sunsetToMidnight.append(sunset + timedelta(seconds=i*interval))
    sunsetToMidnight.append(timedelta(days=1))

    toReturn = midnightToSunrise + sunriseToSunset + sunsetToMidnight

    return toReturn

def changeWallpaper(pathToWallpaper: str):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, pathToWallpaper, 0)

def getCurrentTime() -> timedelta:
    timeToReturn = localtime()
    timeToReturn = timedelta(seconds=(timeToReturn.tm_hour * 60 + timeToReturn.tm_min) * 60 + timeToReturn.tm_sec)
    return timeToReturn

def calculateDaytime(lat: float, long: float) -> tuple[timedelta, timedelta]:
    timeZoneLocal = timezone if localtime().tm_isdst == 0 else altzone
    timeZoneLocal *= -1

    sunriseInSecs = Astral().sunrise_utc(date.today(), lat, long)
    sunriseInSecs = (sunriseInSecs.hour * 60 + sunriseInSecs.minute) * 60 + sunriseInSecs.second
    sunriseInSecs += timeZoneLocal

    sunsetInSecs = Astral().sunset_utc(date.today(), lat, long)
    sunsetInSecs = (sunsetInSecs.hour * 60 + sunsetInSecs.minute) * 60 + sunsetInSecs.second
    sunsetInSecs += timeZoneLocal

    return timedelta(seconds=sunriseInSecs), timedelta(seconds=sunsetInSecs)

def chooseWallpaper(dayIntervals: list[timedelta], currentTime:timedelta) -> int:
    for intervalStart in dayIntervals:
        if currentTime < intervalStart:
            return dayIntervals.index(intervalStart)

def sortWallpapers(l: list[str]) -> list[str]:
    indexList = [int(i.split("_")[-1].split(".")[0]) for i in l]
    indexList.sort()
    sortedList = []
    #Yes its O(n^2), deal with it
    for i in indexList:
        for j in l:
            if i == int(j.split("_")[-1].split(".")[0]):
                sortedList.append(j)
                break
    return sortedList

def initialiseRelevantVariables(relativePath: str) -> tuple[list[str], list[timedelta]]:
    #Converts relative path to absolute path
    pathToWallpapers = os.path.abspath(relativePath)
    wallpapersIterator = os.scandir(pathToWallpapers)
    #List of absolute paths for each wallpaper
    pathToWallpaper = [i.path for i in wallpapersIterator]
    pathToWallpaper = sortWallpapers(pathToWallpaper)
    dayIntervals = splitDayIntoParts(len(pathToWallpaper))

    return pathToWallpaper, dayIntervals

def wallpaperChangingLoop():
    previousIndex = -1
    while True:
        print("Entered loop")
        currentTime = getCurrentTime()
        currentIndex = chooseWallpaper(dayIntervals, currentTime)
        print(f"currentTime: {currentTime}, currentIndex: {currentIndex}, previousIndex: {previousIndex}")
        #Makes sure wallpaper isn't changed constantly
        if currentIndex != previousIndex:
            changeWallpaper(pathToWallpaper[currentIndex])
            print("Wallpaper changed")
            previousIndex = currentIndex
        sleep(30)

if __name__ == '__main__':
    #Relative path to wallpapers folder
    #In the future should be changed trough a GUI to select wallpaper batch
    with open("config", "r") as config:
        relativePath = config.readline().replace(" ", "").split(":")[1][:-1]
        longitude = int(config.readline().replace(" ", "").split(":")[1])
        latitude = int(config.readline().replace(" ", "").split(":")[1])

    pathToWallpaper, dayIntervals = initialiseRelevantVariables(relativePath)

    #Should be run in a new thread when GUI is implemented
    #wallpaperLoopThread = Thread(target=wallpaperChangingLoop, args=(pathToWallpaper, dayIntervals))
    #wallpaperLoopThread.start()
    wallpaperChangingLoop()

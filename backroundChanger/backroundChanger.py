import ctypes
import os
from datetime import timedelta, datetime
from time import sleep, localtime
import math
#from threading import Thread

#---
#Src: https://stackoverflow.com/questions/31142181/calculating-julian-date-in-python
def getJulianDatetime(date: datetime) -> float:
    """
    Convert a datetime object into julian float.
    Args:
        date: datetime-object of date in question

    Returns: float - Julian calculated datetime.
    Raises:
        TypeError : Incorrect parameter type
        ValueError: Date out of range of equation
    """

    # Ensure correct format
    if not isinstance(date, datetime):
        raise TypeError('Invalid type for parameter "date" - expecting datetime')
    elif not(1801 <= date.year <= 2099):
        raise ValueError('Datetime must be between year 1801 and 2099')

    # Perform the calculation
    julianDatetime = 367 * date.year - int((7 * (date.year + int((date.month + 9) / 12.0))) / 4.0) + \
                     int((275 * date.month) / 9.0) + \
                     date.day + 1721013.5 + \
                     (date.hour + date.minute / 60.0 + date.second / math.pow(60, 2)) / 24.0 - \
                     0.5 * math.copysign(1, 100 * date.year + date.month - 190002.5) + 0.5

    return julianDatetime
#---

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
    julianDate = getJulianDatetime(datetime.today())
    n = julianDate - 2451545 + 0.0008 #Julian day
    jStar = n - long/360 #Mean solar time
    m = (357.5291 + 0.98560028 * jStar) % 360 #Solar mean anomaly
    c = 1.9148 * math.sin(m) + 0.0200 * math.sin(2 * m) + 0.0003 * math.sin(3 * m) #Equation of the center
    lam = (m + c + 180 + 102.9372)%360 #Ecliptic longitude
    jTransit = 2451545 + jStar + 0.0053 * math.sin(m) - 0.0069 * math.sin(2 * lam) #Solar transit
    delta = math.asin(math.sin(lam) * math.sin(23.44)) #Declination of the Sun
    omega = math.acos((math.sin(-0.83) - math.sin(lat) * math.sin(delta)) / (math.cos(lat) * math.cos(delta))) #Hour angle
    jRise = jTransit - omega/360 #Julian date of sunrise
    jSet = jTransit + (omega + 180)/360 #Julian date of sundown

    sunriseInSecs = (jRise - int(jRise)) * (24 * 60 * 60)

    sunsetInSecs = (jSet - int(jSet)) * (24 * 60 * 60)

    return timedelta(seconds=sunriseInSecs), timedelta(seconds=sunsetInSecs)

def chooseWallpaper(dayIntervals: list[timedelta], currentTime:timedelta) -> int:
    for intervalStart in dayIntervals:
        if currentTime < intervalStart:
            return dayIntervals.index(intervalStart)

def sortWallpapers(l: list[str]) -> list[str]:
    indexList = [int(i.split("_")[-1].split(".")[0]) for i in l]
    indexList.sort()
    sortedList = []
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
        # Makes sure wallpaper isn't changed constantly
        if currentIndex != previousIndex:
            changeWallpaper(pathToWallpaper[currentIndex])
            print("Wallpaper changed")
            previousIndex = currentIndex
        sleep(30)

if __name__ == '__main__':
    #Relative path to wallpapers folder
    #In the future should be changed trough a GUI to select wallpaper batch
    with open("config.conf", "r") as config:
        relativePath = config.readline().replace(" ", "").split(":")[1][:-1]
        longitude = int(config.readline().replace(" ", "").split(":")[1])
        latitude = int(config.readline().replace(" ", "").split(":")[1])

    pathToWallpaper, dayIntervals = initialiseRelevantVariables(relativePath)

    #Should be run in a new thread when GUI is implemented
    #wallpaperLoopThread = Thread(target=wallpaperChangingLoop, args=(pathToWallpaper, dayIntervals))
    #wallpaperLoopThread.start()
    wallpaperChangingLoop()

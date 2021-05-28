import ctypes
import os
from datetime import timedelta
from time import time, sleep


def splitDayIntoParts(n: int) -> list[timedelta]:
    secsInADay = 24 * 60 * 60
    interval = secsInADay / n
    returnList = []
    for i in range(1, n+1):
        returnList.append(timedelta(seconds=interval*i))

    return returnList

def changeWallpaper(pathToWallpaper: str):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, pathToWallpaper, 0)

def getCurrentTime() -> timedelta:
    timeToReturn = time()
    timeToReturn = timedelta(seconds=(timeToReturn - timedelta(seconds=timeToReturn).days*24*60*60))
    return timeToReturn

def chooseWallpaper(dayIntervals: list[timedelta], currentTime:timedelta) -> int:
    for intervalStart in dayIntervals:
        if currentTime < intervalStart:
            return dayIntervals.index(intervalStart)

if __name__ == '__main__':
    #Absolute path is necessary for the wallpaper path
    pathToWallpapers = os.path.abspath("wallpapers")
    wallpapersIterator = os.scandir(pathToWallpapers)

    pathToWallpaper = [i.path for i in wallpapersIterator]
    dayIntervals = splitDayIntoParts(len(pathToWallpaper))

    previousIndex = 0
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


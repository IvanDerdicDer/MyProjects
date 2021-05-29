import ctypes
import os
from datetime import timedelta
from time import time, sleep
from threading import Thread


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

def initialiseRelevantVariables(relativePath: str):
    #Converts relative path to absolute path
    pathToWallpapers = os.path.abspath(relativePath)
    wallpapersIterator = os.scandir(pathToWallpapers)
    #List of absolute paths for each wallpaper
    pathToWallpaper = [i.path for i in wallpapersIterator]
    dayIntervals = splitDayIntoParts(len(pathToWallpaper))

    return pathToWallpaper, dayIntervals

def wallpaperChangingLoop(pathToWallpaper: list[str], dayIntervals: list[timedelta]):
    previousIndex = 0
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
    relativePath = "wallpapers"

    pathToWallpaper, dayIntervals = initialiseRelevantVariables(relativePath)

    #Should be run in a new thread when GUI is implemented
    #wallpaperLoopThread = Thread(target=wallpaperChangingLoop, args=(pathToWallpaper, dayIntervals))
    #wallpaperLoopThread.start()
    wallpaperChangingLoop(pathToWallpaper, dayIntervals)

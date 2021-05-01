from bisect import bisect_right
from random import randint
from time import thread_time

inputArray = [randint(-1000000, 1000000) for _ in range(1000000)]
#inputArray = [1, 5, -2, 6, -3, 9, 12, -63, 83]
#inputArray = [1, 1, 1,-4,-5,-1,-8,-12]

def firstMissingPositive(arr: list):
    #Array needs to be sorted for bisect
    if 1 not in arr:
        return 1
    arr.sort()
    #This lambda ensures that only positive ints are considered
    smallestPositiveInt = 1
    #By using bisect_right we get the index of the second smallest int
    startIndex = bisect_right(arr, smallestPositiveInt)
    #Move trough the list until the next smallest number is bigger than smallest number + 1
    length = len(arr)
    while startIndex < length and (arr[startIndex] == smallestPositiveInt + 1):
        #Set the next smallest number
        smallestPositiveInt = arr[startIndex]
        #Find the index of the next smallest number
        startIndex = bisect_right(arr, smallestPositiveInt)


    return smallestPositiveInt + 1

if __name__ == '__main__':
    useArr = inputArray.copy()
    print("Starting...")
    listOfTimes = []
    for _ in range(10):
        useArr = [randint(-1000000, 1000000) for _ in range(1000000)]
        startTimeMs = thread_time()
        result = firstMissingPositive(useArr)
        endTimeMs = thread_time()
        listOfTimes.append(endTimeMs-startTimeMs)

    print(f"Average time: {sum(listOfTimes)/len(listOfTimes)} s")

from bisect import bisect_right
from random import randint
from time import time

#inputArray = [randint(-1000000, 1000000) for _ in range(10000000)]
inputArray = [1, 5, -2, 6, -3, 9, 12, -63, 83]

def firstMissingPositive(arr: list):
    #This lambda ensures that only positive ints are considered
    smallestPositiveInt = min(arr, key= lambda k: k < 0)
    #By using bisect_right we get the index of the second smallest int
    startIndex = bisect_right(arr, smallestPositiveInt)
    #Move trough the list until the next smallest number is bigger than smallest number + 1
    while arr[startIndex] == smallestPositiveInt + 1:
        #Set the next smallest number
        smallestPositiveInt = arr[startIndex]
        #Find the index of the next smallest number
        startIndex = bisect_right(arr, smallestPositiveInt)

    return smallestPositiveInt + 1

useArr = inputArray.copy()
startTimeMs = time()
result = firstMissingPositive(useArr)
endTimeMs = time()
print(f"Result: {result} Runtime: {endTimeMs - startTimeMs} ms")
print(f"InputArray : {inputArray}")
print(f"UsedArray: {useArr}")
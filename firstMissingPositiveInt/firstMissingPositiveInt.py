from bisect import bisect_right
from random import randint
from time import thread_time
from math import ceil

inputArray = [randint(-1000000, 1000000) for _ in range(1000000)]
#inputArray = [1, 5, -2, 6, -3, 9, 12, -63, 83]
#inputArray = [1, 1, 1,-4,-5,-1,-8,-12]

def bucketSort(arr):
    numberOfElements = int(ceil(max(arr)/256))
    bucket = {}
    l = [0]*numberOfElements if numberOfElements else [0]
    for i in arr:
        if i > 0:
            if i not in bucket.keys():
                bucket[i] = 0
                l[i%numberOfElements] |= 1 << (i%numberOfElements)%256
            bucket[i] += 1
    outList = []
    for i in l:
        for j in range(256):
            if i & (1 << j):
                outList += [i * 256 + j] * bucket[i * 256 + j]


def firstMissingPositive(arr: list):
    if 1 not in arr:
        return 1
    #Array needs to be sorted for bisect
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

from time import  thread_time
from math import sqrt

def isPrime(n):
    if n == 1:
        return False
    prime = 0
    for i in range(2, n):
        if n % i == 0:
            prime += 1
        if prime > 1:
            return False
    return True

def allPrimes(arr: list):
    for i in arr:
        if not isPrime(i):
            return False
    return True

def isPrime2(n: int, arr: list):
    if not arr:
        return True
    for i in arr:
        if n % i == 0:
            return False
    return True

def eratosthenesSieve(arr: list, n):
    i = 0
    length = sqrt(n)
    while i < length:
        for j in arr:
            if j%arr[i] == 0 and j != arr[i]:
                arr.remove(j)

        i += 1
    return arr

if __name__ == '__main__':
    n = 10000
    listOfNumbers = [2]+[i for i in range(3, n, 2)]
    listToUse = listOfNumbers.copy()
    numberOfPrimes = 1

    primes = eratosthenesSieve(listToUse, n)

    print(f"ListOfNumbers: {primes}\nlen: {len(primes)}\nallPrimes: {allPrimes(primes)}")

    startTime = thread_time()
    numberOfPasses = 0
    endTime = thread_time()
    while endTime - startTime < 5:
        eratosthenesSieve(listToUse, n)
        numberOfPasses += 1
        endTime = thread_time()

    print(f"NumberOfPasses: {numberOfPasses} Runtime: {endTime-startTime}")


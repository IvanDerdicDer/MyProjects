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
    length = sqrt(n)
    for i in range(int(length)):
        for j in arr:
            if j%arr[i] == 0 and j != arr[i]:
                arr.remove(j)
    return arr

def eratosthenesSieve2(arr: list):
    primes = []
    for j in arr:
        if isPrime2(j, primes):
            primes.append(j)
    return primes

if __name__ == '__main__':
    n = 1000
    listOfNumbers = [2]+ list(range(3, n, 2))

    primes = eratosthenesSieve(listOfNumbers.copy(), n)

    #print(f"ListOfNumbers: {primes}\nlen: {len(primes)}\nallPrimes: {allPrimes(primes)}")
    print(f"ListOfNumbers: {primes}\nlen: {len(primes)}")

    print(f"Starting 1")
    startTime = thread_time()
    numberOfPasses = 0
    endTime = thread_time()
    while endTime - startTime < 5:
        eratosthenesSieve(listOfNumbers.copy(), n)
        numberOfPasses += 1
        endTime = thread_time()

    print(f"NumberOfPasses: {numberOfPasses} Runtime: {endTime-startTime}\n")

    primes = eratosthenesSieve2(listOfNumbers)

    print(f"ListOfNumbers: {primes}\nlen: {len(primes)}")

    print(f"Starting 2")
    startTime = thread_time()
    numberOfPasses = 0
    endTime = thread_time()
    while endTime - startTime < 5:
        eratosthenesSieve2(listOfNumbers)
        numberOfPasses += 1
        endTime = thread_time()

    print(f"NumberOfPasses: {numberOfPasses} Runtime: {endTime - startTime}")


from time import  thread_time

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

def eratosthenesSieve(arr: list):
    i = 0
    primes = []
    length = len(arr)
    while i < length:
        if isPrime2(arr[i], primes):
            primes.append(arr[i])

        i += 1
    return primes

if __name__ == '__main__':
    n = 1000
    listOfNumbers = [i for i in range(3, n, 2)]
    listToUse = listOfNumbers.copy()
    numberOfPrimes = 1

    primes = eratosthenesSieve(listToUse)
    primes.insert(0, 2)

    print(f"ListOfNumbers: {primes}\nlen: {len(primes)}\nallPrimes: {allPrimes(primes)}")

    startTime = thread_time()
    numberOfPasses = 0
    endTime = thread_time()
    while endTime - startTime < 5:
        eratosthenesSieve(listToUse)
        numberOfPasses += 1
        endTime = thread_time()

    print(f"NumberOfPasses: {numberOfPasses} Runtime: {endTime-startTime}")


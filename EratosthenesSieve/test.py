import sieve
from time import thread_time

if __name__ == '__main__':
    n = 10000
    primes = sieve.eratosthenesSieve5(n)

    print(f"ListOfNumbers: {primes}\nlen: {len(primes)}")

    print(f"Starting 5")
    startTime = thread_time()
    numberOfPasses = 0
    endTime = thread_time()
    while endTime - startTime < 5:
        sieve.eratosthenesSieve5(n)
        numberOfPasses += 1
        endTime = thread_time()

    print(f"NumberOfPasses: {numberOfPasses} Runtime: {endTime - startTime}\n")

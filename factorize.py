from time import time
from multiprocessing import Pool
from concurrent.futures import ProcessPoolExecutor

def factorize(num):
    factors = []
    for i in range(1, num + 1):
        if num % i == 0:
            factors.append(i)
    return factors

def parallel_factorize(*nums):
    with Pool() as pool:
        result = pool.map(factorize, nums)
    return result

#def parallel_factorize2(*nums):
#    with ProcessPoolExecutor() as executor:
#        result = list(executor.map(factorize, nums))
#    return result

if __name__ == '__main__':
    numbers = [128, 255, 99999, 10651060, 23456789, 98765432]
    start = time()
    print(parallel_factorize(*numbers))
    #for i in numbers:
    #    print(factorize(i))
    end = time()
    print(f"Execution time: {end - start:.2f} seconds.")
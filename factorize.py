from multiprocessing import Pool, cpu_count
from time import time, sleep

def factorize(*number):
    divider_list = []
    for num in number:
        num_list = []        
        for i in range(1, num + 1):
            if num % i == 0:
                num_list.append(i)
        divider_list.append(num_list)
    return divider_list

if __name__ == "__main__":
    start = time()
    a, b, c, d = factorize(128, 255, 99999, 10651060)
    sleep(0.5)
    end = time()
    print(f'Synchronous function execution time: {end - start} sec')

    with Pool(cpu_count()) as p:
        start = time()
        results = p.map(factorize, (128, 255, 99999, 10651060))
        sleep(0.5)
        end = time()
        print(f'Execution time of the optimized version: {end - start} sec')
        p.close()
        p.join()
    

                       


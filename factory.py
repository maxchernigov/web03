# def factorize(*number):
#     # YOUR CODE HERE
#     raise NotImplementedError()


# a, b, c, d  = factorize(128, 255, 99999, 10651060)

# assert a == [1, 2, 4, 8, 16, 32, 64, 128]
# assert b == [1, 3, 5, 15, 17, 51, 85, 255]
# assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
# assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]


import multiprocessing
import time


def factorize_sync(*numbers):
    result = []
    for num in numbers:
        divisors = [i for i in range(1, num + 1) if num % i == 0]
        result.append(divisors)
    return result


def factorize_parallel(*numbers):
    num_cores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(num_cores)
    results = pool.map(factorize_number, numbers)
    pool.close()
    pool.join()
    return results


def factorize_number(num):
    return [i for i in range(1, num + 1) if num % i == 0]


if __name__ == '__main__':
    start_time = time.time()
    a, b, c, d = factorize_sync(128, 255, 99999, 10651060)
    end_time = time.time()
    print("Синхронна версія зайняла час: {:.4f} секунд".format(end_time - start_time))

    start_time = time.time()
    e, f, g, h = factorize_parallel(128, 255, 99999, 10651060)
    end_time = time.time()
    print("Покращена версія з багатьма ядрами зайняла час: {:.4f} секунд".format(end_time - start_time))
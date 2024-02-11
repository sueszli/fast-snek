import os
from concurrent.futures import ProcessPoolExecutor


def fib(n):
    return n if n < 2 else fib(n - 2) + fib(n - 1)


if __name__ == "__main__":
    cores = os.cpu_count()
    with ProcessPoolExecutor(max_workers=cores) as executor:
        results = executor.map(fib, range(35))

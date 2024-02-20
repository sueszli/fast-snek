import ctypes
import os
import threading

path = os.path.join(os.path.dirname(__file__), "fibonacci.so")
fibonacci = ctypes.CDLL(path)

for _ in range(os.cpu_count()):
    arg = 35
    threading.Thread(target=fibonacci.fib, args=(arg,)).start()

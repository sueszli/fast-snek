import ctypes
import os
import threading

path = os.path.join(os.path.dirname(__file__), "fibonacci.so")
fibonacci = ctypes.CDLL(path)

fib = fibonacci.fib
fib.argtypes = (ctypes.c_int,)
fib.restype = ctypes.c_int

for _ in range(os.cpu_count()):
    arg = 35
    threading.Thread(target=fib, args=(arg,)).start()

import cython


# @ccall: call c code from below
@cython.ccall
def fib(n: cython.int) -> cython.int:
    # nogil: release GIL
    with cython.nogil:
        return _fib(n)


# @cfunc: generate c function
# @nogil: thread-safe
# @exceptval: never raises exceptions
@cython.cfunc
@cython.nogil
@cython.exceptval(check=False)
def _fib(n: cython.int) -> cython.int:
    return n if n < 2 else _fib(n - 2) + _fib(n - 1)


if not cython.compiled:
    import sys

    sys.stderr.write("please first compile the module with cython\n")

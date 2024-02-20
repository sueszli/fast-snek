the cpython interpreter is already pretty good at io-bound tasks through async/await.

but the GIL (global interpreter lock) hinders thread-parallelism in cpu-bound tasks.

you currently can only achieve parallelism in python through multiprocessing, which is not ideal for many use-cases.

the community is actively working on this by either trying to introduce multiple sub-interpreters [^subint1] [^subint2] or making the GIL optional [^nogil1] [^nogil2] [^nogil3].

until then, we have to use workarounds in python or superset programming languages [^superset1] [^superset2].

<br><br>

# parallel programming in python

**_1) multiprocessing_**

- https://docs.python.org/3/library/multiprocessing.html (same api as `threading`, so they're interchangable)
- https://docs.python.org/3/library/concurrent.futures.html (same functionality but more java-like)

- multiple system processes, each with their own seperate python interpreter, GIL and memory space.

- pros:
     - very simple.
     - high cpu priority. the os always prioritizes processes over threads which can make a difference for specific types of parallelization.
     - high memory isolation and safety.
- cons:
     - data serialization overhead: there is no shared memory, so data has to be serialized and deserialized for inter-process communication.
     - some objects are unserializeable: the `pickle` module is used to serialize objects. but some objects are not pickleable (i.e. lambdas, file handles, etc.).
     - creation overhead: slow creation, destruction and management, because we are context-switching to the os to manage system processes.

<br>

**_2) c extension modules_**

- https://docs.python.org/3/extending/extending.html

- we can write extension modules to cpython where the GIL is released and call them from python's kernel-level [^thread] threads.
- the rust extension libraries are promising and used in some new popular projects [^rust1] [^rust2] but contain unsafe code [^rustunsafe] and are generally still immature.
- alternatively you can also use cython (not to be confused with cpython) to generate the c-code for the extension in python. cython is used in some popular projects like numpy and lxml. but the weird syntax makes it less versatile.

- pros:
     - bare metal level performance.
- cons:
     - requires very api-specific knowledge and a lot of boilerplate code.
     - not portable: you have to link the python source code to build your project.

<br>

**_3) ctypes / foreign function interface (ffi)_**

- https://docs.python.org/3/library/ctypes.html

- calling a foreign function, not from python but from the underlying cpython interpreter.
- doesn't require any wrapping in extension modules. you can use any binary (as a .so or .dll) as long as it has a c interface.
- you don't need to manage the gil. it is automatically released when calling the foreign function [^release].

- pros:
     - bare metal level performance.
     - works with any binary.
     - easy to understand. doesn't require any api-specific knowledge.
     - more portable than c-extension modules. isn't specific to just the cpython implementation.
- cons:
     - data serialization overhead: automatic type conversions done by the ffi-library are very expensive [^ctypebad] → but fortunately this can be circumvented by passing pointers.

<br><br>

# references

- https://realpython.com/python-parallel-processing/#make-python-threads-run-in-parallel
- https://github.com/realpython/materials/tree/master/python-parallel-processing/

[^subint1]: https://peps.python.org/pep-0554/
[^subint2]: https://peps.python.org/pep-0683/
[^nogil1]: https://peps.python.org/pep-0703/
[^nogil2]: https://discuss.python.org/t/a-steering-council-notice-about-pep-703-making-the-global-interpreter-lock-optional-in-cpython/30474
[^nogil3]: https://engineering.fb.com/2023/10/05/developer-tools/python-312-meta-new-features/
[^superset1]: https://www.taichi-lang.org/
[^superset2]: https://docs.modular.com/mojo/stdlib/python/python.html
[^thread]: https://stackoverflow.com/questions/46212711/python-threading-module-creates-user-space-threads-or-kernel-spece-threads
[^rust1]: https://github.com/PyO3/pyo3/blob/main/guide/src/parallelism.md#parallelism
[^rust2]: https://github.com/pola-rs/polars
[^rustunsafe]: https://users.rust-lang.org/t/python-rust-interop/30243/12
[^release]: https://docs.python.org/3/library/ctypes.html#:~:text=released%20before%20calling
[^ctypebad]: https://stackoverflow.com/a/8069179/13045051

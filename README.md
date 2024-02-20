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

- extending cpython with modules in which the gil is manually released. we can then call those modules in multithreaded python code.
- the rust extension libraries are promising and used in some new popular projects [^rust1] [^rust2] but contain unsafe code [^rustunsafe] and are generally still too immature.
- alternatively you can also use cython (not to be confused with cpython) for code generation. it's used by numpy and lxml but a lot more limiting than writing the extension modules by hand in c.

- pros:
     - very performant.
- cons:
     - very complex api. data isn't marshalled automatically.
     - not portable. we must link cpython during the build step to extend it. but fortunately there are nice build tools to simplify this [^setuptools].

<br>

**_3) ctypes / foreign function interface (ffi)_**

- https://docs.python.org/3/library/ctypes.html
- https://cffi.readthedocs.io/en/stable/overview.html#main-mode-of-usage

- accessing a shared library in c (or any other language providing a c interface [^nogolang]). we can then call those libraries in multithreaded python code.

- pros:
     - very performant.
     - very simple.
     - gil is released automatically on each foreign function call [^release].
- cons:
     - data serialization overhead: automatic type conversions done by the ffi-library are very expensive [^ctypebad]. but fortunately this can be circumvented by passing pointers.

<br><br>

# references

- https://realpython.com/python-parallel-processing/#make-python-threads-run-in-parallel
- https://github.com/realpython/materials/tree/master/python-parallel-processing/
- https://github.com/mattip/c_from_python/blob/master/c_from_python.ipynb

[^subint1]: https://peps.python.org/pep-0554/
[^subint2]: https://peps.python.org/pep-0683/
[^nogil1]: https://peps.python.org/pep-0703/
[^nogil2]: https://discuss.python.org/t/a-steering-council-notice-about-pep-703-making-the-global-interpreter-lock-optional-in-cpython/30474
[^nogil3]: https://engineering.fb.com/2023/10/05/developer-tools/python-312-meta-new-features/
[^superset1]: https://www.taichi-lang.org/
[^superset2]: https://docs.modular.com/mojo/stdlib/python/python.html
[^rust1]: https://github.com/PyO3/pyo3/blob/main/guide/src/parallelism.md#parallelism
[^rust2]: https://github.com/pola-rs/polars
[^rustunsafe]: https://users.rust-lang.org/t/python-rust-interop/30243/12
[^release]: https://docs.python.org/3/library/ctypes.html#:~:text=released%20before%20calling
[^ctypebad]: https://stackoverflow.com/a/8069179/13045051
[^nogolang]: https://stackoverflow.com/questions/70349271/ctypes-calling-go-dll-with-arguments-c-string
[^setuptools]: https://setuptools.pypa.io/

the cpython interpreter is already pretty good at io-bound tasks through async/await.

but the GIL (global interpreter lock) hinders parallelism for cpu-bound tasks.

the community is actively working on this by either trying to introduce multiple sub-interpreters [^subint1] [^subint2] or making the GIL optional [^nogil1] [^nogil2] [^nogil3].

until then, we have to use workarounds.

<br><br>

## parallelism in python

_multiprocessing_

- this is the intended way: by running multiple system processes, each with its python interpreter that has its own GIL and memory space.

- https://docs.python.org/3/library/multiprocessing.html
- https://docs.python.org/3/library/concurrent.futures.html (same functionality but inspired by java)

- pros:
     - simple to implement and understand, drop-in replacement for threading.
     - high cpu priority (the os usually prioritizes processes over threads).
     - high memory isolation and safety.
- cons:

     - data serialization overhead: there is no shared memory, so data has to be serialized and deserialized for inter-process communication.
     - some objects are unserializeable: the `pickle` module is used to serialize objects, and some objects are not pickleable (i.e. lambdas, file handles, etc.).
     - creation overhead: slow creation, destruction and management, because we are context-switching to the os to manage system processes.
     - not portable: processes are managed differently in each operating system.

<br><br>

_c extensions for (parallel) multithreading_

- we can write extension modules to cpython where the GIL is released and call them from python.

- c/c++: https://docs.python.org/3/extending/extending.html
- rust: https://github.com/PyO3/pyo3/blob/main/guide/src/parallelism.md#parallelism → relatively new but promising. used in the [polars](https://github.com/pola-rs/polars) project. but contains some [unsafe code](https://users.rust-lang.org/t/python-rust-interop/30243/12) that might be a security risk.

<br><br>

_cython_

- https://cython.org/

- c-extension code generator. used to be a superset language of python but is now a library.
- trusted by numpy, lxml, etc.

<br><br>

_mojo lang_

- superset language of python. still in its infancy, but it has a lot of potential.

- https://docs.modular.com/mojo/stdlib/python/python.html

<br><br>

## references

- https://realpython.com/python-parallel-processing/#make-python-threads-run-in-parallel
- https://github.com/realpython/materials/tree/master/python-parallel-processing/

[^subint1]: https://peps.python.org/pep-0554/
[^subint2]: https://peps.python.org/pep-0683/
[^nogil1]: https://peps.python.org/pep-0703/
[^nogil2]: https://discuss.python.org/t/a-steering-council-notice-about-pep-703-making-the-global-interpreter-lock-optional-in-cpython/30474
[^nogil3]: https://engineering.fb.com/2023/10/05/developer-tools/python-312-meta-new-features/

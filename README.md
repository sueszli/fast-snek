python (the cpython implementation) is already pretty good at io-bound tasks through async/await.

but the GIL (global interpreter lock) hinders parallelism for cpu-bound tasks.

the community is actively working on this by either introducing multiple sub-interpreters [^1] [^2] or making the GIL optional [^3] [^4] [^5].

until then, we have to use workarounds.

- multiprocessing

     - https://docs.python.org/3/library/multiprocessing.html
     - https://docs.python.org/3/library/concurrent.futures.html (same functionality but inspired by java, more high level)

     - this is the intended way: by running multiple system processes, each with its python interpreter that has its own GIL and memory space.

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

## references

- https://realpython.com/python-parallel-processing/#make-python-threads-run-in-parallel
- https://github.com/realpython/materials/tree/master/python-parallel-processing/

[^1]: https://peps.python.org/pep-0554/
[^2]: https://peps.python.org/pep-0683/
[^3]: https://peps.python.org/pep-0703/
[^4]: https://discuss.python.org/t/a-steering-council-notice-about-pep-703-making-the-global-interpreter-lock-optional-in-cpython/30474
[^5]: https://engineering.fb.com/2023/10/05/developer-tools/python-312-meta-new-features/

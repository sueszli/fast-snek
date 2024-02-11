- https://realpython.com/python-parallel-processing/

- https://github.com/realpython/materials/tree/master/python-parallel-processing/

---

python's cpython implementation is already pretty good at io-bound tasks through async/await. but the GIL (global interpreter lock) makes hinders parallelism for cpu-bound tasks.

the community is actively working on this:

- using multiple sub-interpreters
     - https://peps.python.org/pep-0554/
     - https://peps.python.org/pep-0683/
- making the gil optional
     - https://peps.python.org/pep-0703/
     - https://discuss.python.org/t/a-steering-council-notice-about-pep-703-making-the-global-interpreter-lock-optional-in-cpython/30474
     - https://engineering.fb.com/2023/10/05/developer-tools/python-312-meta-new-features/

until then, we have to use workarounds.

# workarounds

- multiprocessing
     - running multiple python processes/interpreters each with their own GIL and memory space.
     - pros:
          - simple to implement
          - high cpu priority (the os usually prioritizes processes over threads)
          - high memory isolation and safety
     - cons:
          - no shared memory, so data has to be serialized and deserialized
          - high overhead for creating, destroying, and inter-process communication

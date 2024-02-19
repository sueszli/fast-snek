#include <Python.h>

// implementation
int fib(int n) {
    return n < 2 ? n : fib(n - 2) + fib(n - 1);
}

// python wrapper: 
// 1. PyArg_ParseTuple: parse the input arguments as C types
// 2. Py_BEGIN_ALLOW_THREADS: release the GIL
// 3. Py_END_ALLOW_THREADS: reacquire the GIL
// 4. Py_BuildValue: convert to Python types
static PyObject* fibmodule_fib(PyObject* self, PyObject* args) {
    int n;
    int result;

    if (!PyArg_ParseTuple(args, "i", &n)) {
        return NULL;
    }

    Py_BEGIN_ALLOW_THREADS
    result = fib(n);
    Py_END_ALLOW_THREADS

    return Py_BuildValue("i", result);
}

// module definition:
// - PyMethodDef: list of methods
// - PyModuleDef: module definition
// - PyMODINIT_FUNC: module initialization function
static PyMethodDef fib_methods[] = {
    {"fib", fibmodule_fib, METH_VARARGS, "Calculate the nth Fibonacci"},
    {NULL, NULL, 0, NULL}
};
static struct PyModuleDef fibmodule = {
    PyModuleDef_HEAD_INIT,
    "fibmodule",
    "Efficient Fibonacci number calculator",
    -1,
    fib_methods
};
PyMODINIT_FUNC PyInit_fibmodule(void) {
    return PyModule_Create(&fibmodule);
}

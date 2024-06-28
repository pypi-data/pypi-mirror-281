#include <Python.h>

static PyObject* foo(PyObject* self)
{
    return PyUnicode_FromString("bar");
}

static PyMethodDef methods[] = {
    {"foo", (PyCFunction)foo, METH_NOARGS, NULL},
    {NULL, NULL, 0, NULL},
};

static struct PyModuleDef module = {
    PyModuleDef_HEAD_INIT,
    "runge_kutta_4_calcs",
    NULL,
    -1,
    methods,
};

PyMODINIT_FUNC PyInit_runge_kutta_4_calcs(void)
{
    return PyModule_Create(&module);
}
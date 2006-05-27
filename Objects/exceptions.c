#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "structmember.h"
#include "osdefs.h"

#define MAKE_IT_NONE(x) (x) = Py_None; Py_INCREF(Py_None);
#define EXC_MODULE_NAME "exceptions."

/*
 *    BaseException
 */
static PyObject *
BaseException_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    PyBaseExceptionObject *self;

    self = (PyBaseExceptionObject *)type->tp_alloc(type, 0);
    /* the dict is created on the fly in PyObject_GenericSetAttr */
    self->message = self->dict = NULL;

    self->args = PyTuple_New(0);
    if (!self->args) {
        Py_DECREF(self);
        return NULL;
    }

    self->message = PyString_FromString(""); 
    if (!self->message) {
        Py_DECREF(self);
        return NULL;
    }

    return (PyObject *)self;
}

static int
BaseException_init(PyBaseExceptionObject *self, PyObject *args, PyObject *kwds)
{
    Py_DECREF(self->args);
    self->args = args;
    Py_INCREF(self->args);

    if (PyTuple_GET_SIZE(self->args) == 1) {
        Py_DECREF(self->message);
        self->message = PyTuple_GET_ITEM(self->args, 0);
	Py_INCREF(self->message);
    }
    return 0;
}

int
BaseException_clear(PyBaseExceptionObject *self)
{
    Py_CLEAR(self->dict);
    Py_CLEAR(self->args);
    Py_CLEAR(self->message);
    return 0;
}

static void
BaseException_dealloc(PyBaseExceptionObject *self)
{
    BaseException_clear(self);
    self->ob_type->tp_free((PyObject *)self);
}

int
BaseException_traverse(PyBaseExceptionObject *self, visitproc visit, void *arg)
{
    if (self->dict)
        Py_VISIT(self->dict);
    Py_VISIT(self->args);
    Py_VISIT(self->message);
    return 0;
}

static PyObject *
BaseException_str(PyBaseExceptionObject *self)
{
    PyObject *out;

    switch (PySequence_Length(self->args)) {
    case 0:
        out = PyString_FromString("");
        break;
    case 1:
    {
        PyObject *tmp = PySequence_GetItem(self->args, 0);
        if (tmp) {
            out = PyObject_Str(tmp);
            Py_DECREF(tmp);
        }
        else
            out = NULL;
        break;
    }
    case -1:
        PyErr_Clear();
        /* Fall through */
    default:
        out = PyObject_Str(self->args);
        break;
    }

    return out;
}

static PyObject *
BaseException_repr(PyBaseExceptionObject *self)
{
    Py_ssize_t args_len;
    PyObject *repr_suffix;
    PyObject *repr;
    char *name;
    char *dot;

    args_len = PySequence_Length(self->args);
    if (args_len < 0) {
        return NULL;
    }
    
    if (args_len == 0) {
        repr_suffix = PyString_FromString("()");
        if (!repr_suffix)
            return NULL;
    }
    else {
        PyObject *args_repr = PyObject_Repr(self->args);
        if (!args_repr)
            return NULL;
        repr_suffix = args_repr;
    }

    name = (char *)self->ob_type->tp_name;
    dot = strrchr(name, '.');
    if (dot != NULL) name = dot+1;

    repr = PyString_FromString(name);
    if (!repr) {
        Py_DECREF(repr_suffix);
        return NULL;
    }

    PyString_ConcatAndDel(&repr, repr_suffix);
    return repr;
}

/* Pickling support */
static PyObject *
BaseException_reduce(PyBaseExceptionObject *self)
{
    return PyTuple_Pack(3, self->ob_type, self->args, self->dict);
}


#ifdef Py_USING_UNICODE
/* while this method generates fairly uninspired output, it a least
 * guarantees that we can display exceptions that have unicode attributes
 */
static PyObject *
BaseException_unicode(PyBaseExceptionObject *self)
{
    if (PySequence_Length(self->args) == 0)
        return PyUnicode_FromUnicode(NULL, 0);
    if (PySequence_Length(self->args) == 1) {
        PyObject *temp = PySequence_GetItem(self->args, 0);
        PyObject *unicode_obj;
        if (!temp) {
            return NULL;
        }
        unicode_obj = PyObject_Unicode(temp);
        Py_DECREF(temp);
        return unicode_obj;
    }
    return PyObject_Unicode(self->args);
}
#endif /* Py_USING_UNICODE */

static PyMethodDef BaseException_methods[] = {
   {"__reduce__", (PyCFunction)BaseException_reduce, METH_NOARGS },
#ifdef Py_USING_UNICODE
   {"__unicode__", (PyCFunction)BaseException_unicode, METH_NOARGS },
#endif
   {NULL, NULL, 0, NULL},
};



static PyObject *
BaseException_getitem(PyBaseExceptionObject *self, Py_ssize_t index)
{
    return PySequence_GetItem(self->args, index);
}

static PySequenceMethods BaseException_as_sequence = {
    0,                      /* sq_length; */
    0,                      /* sq_concat; */
    0,                      /* sq_repeat; */
    (ssizeargfunc)BaseException_getitem,  /* sq_item; */
    0,                      /* sq_slice; */
    0,                      /* sq_ass_item; */
    0,                      /* sq_ass_slice; */
    0,                      /* sq_contains; */
    0,                      /* sq_inplace_concat; */
    0                       /* sq_inplace_repeat; */
};

static PyMemberDef BaseException_members[] = {
    {"message", T_OBJECT, offsetof(PyBaseExceptionObject, message), 0,
        PyDoc_STR("exception message")},
    {NULL}  /* Sentinel */
};


static PyObject *
BaseException_get_dict(PyBaseExceptionObject *self)
{
    if (self->dict == NULL) {
        self->dict = PyDict_New();
        if (!self->dict)
            return NULL;
    }
    Py_INCREF(self->dict);
    return self->dict;
}

static int
BaseException_set_dict(PyBaseExceptionObject *self, PyObject *val)
{
    if (val == NULL) {
        PyErr_SetString(PyExc_TypeError, "__dict__ may not be deleted");
        return -1;
    }
    if (!PyDict_Check(val)) {
        PyErr_SetString(PyExc_TypeError, "__dict__ must be a dictionary");
        return -1;
    }
    Py_CLEAR(self->dict);
    Py_INCREF(val);
    self->dict = val;
    return 0;
}

static PyObject *
BaseException_get_args(PyBaseExceptionObject *self)
{
    if (self->args == NULL) {
        Py_INCREF(Py_None);
        return Py_None;
    }
    Py_INCREF(self->args);
    return self->args;
}

static int
BaseException_set_args(PyBaseExceptionObject *self, PyObject *val)
{
    PyObject *seq;
    if (val == NULL) {
        PyErr_SetString(PyExc_TypeError, "args may not be deleted");
        return -1;
    }
    seq = PySequence_Tuple(val);
    if (!seq) return -1;
    self->args = seq;
    return 0;
}

static PyGetSetDef BaseException_getset[] = {
    {"__dict__", (getter)BaseException_get_dict, (setter)BaseException_set_dict},
    {"args", (getter)BaseException_get_args, (setter)BaseException_set_args},
    {NULL},
};


static PyTypeObject _PyExc_BaseException = {
    PyObject_HEAD_INIT(NULL)
    0,                          /*ob_size*/
    EXC_MODULE_NAME "BaseException", /*tp_name*/
    sizeof(PyBaseExceptionObject), /*tp_basicsize*/
    0,                          /*tp_itemsize*/
    (destructor)BaseException_dealloc, /*tp_dealloc*/
    0,                          /*tp_print*/
    0,                          /*tp_getattr*/
    0,                          /*tp_setattr*/
    0,                          /* tp_compare; */
    (reprfunc)BaseException_repr, /*tp_repr*/
    0,                          /*tp_as_number*/
    &BaseException_as_sequence, /*tp_as_sequence*/
    0,                          /*tp_as_mapping*/
    0,                          /*tp_hash */
    0,                          /*tp_call*/
    (reprfunc)BaseException_str,  /*tp_str*/
    PyObject_GenericGetAttr,    /*tp_getattro*/
    PyObject_GenericSetAttr,    /*tp_setattro*/
    0,                          /*tp_as_buffer*/
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE | Py_TPFLAGS_HAVE_GC,  /*tp_flags*/
    PyDoc_STR("Common base class for all exceptions"), /* tp_doc */
    (traverseproc)BaseException_traverse, /* tp_traverse */
    (inquiry)BaseException_clear, /* tp_clear */
    0,                          /* tp_richcompare */
    0,                          /* tp_weaklistoffset */
    0,                          /* tp_iter */
    0,                          /* tp_iternext */
    BaseException_methods,      /* tp_methods */
    BaseException_members,      /* tp_members */
    BaseException_getset,       /* tp_getset */
    0,                          /* tp_base */
    0,                          /* tp_dict */
    0,                          /* tp_descr_get */
    0,                          /* tp_descr_set */
    offsetof(PyBaseExceptionObject, dict), /* tp_dictoffset */
    (initproc)BaseException_init, /* tp_init */
    0,                          /* tp_alloc */
    BaseException_new,          /* tp_new */
};
/* the CPython API expects exceptions to be (PyObject *) - both a hold-over
from the previous implmentation and also allowing Python objects to be used
in the API */
PyObject *PyExc_BaseException = (PyObject *)&_PyExc_BaseException;

#define SimpleExtendsException(EXCBASE, EXCNAME, EXCDOC) \
static PyTypeObject _PyExc_ ## EXCNAME = { \
    PyObject_HEAD_INIT(NULL) \
    0, \
    EXC_MODULE_NAME # EXCNAME, \
    sizeof(PyBaseExceptionObject), \
    0, (destructor)BaseException_dealloc, 0, 0, 0, 0, 0, 0, 0, \
    0, 0, 0, 0, 0, 0, 0, \
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE | Py_TPFLAGS_HAVE_GC, \
    PyDoc_STR(EXCDOC), (traverseproc)BaseException_traverse, \
    (inquiry)BaseException_clear, 0, 0, 0, 0, 0, 0, 0, &_ ## EXCBASE, \
    0, 0, 0, offsetof(PyBaseExceptionObject, dict), \
    (initproc)BaseException_init, 0, BaseException_new,\
}; \
PyObject *PyExc_ ## EXCNAME = (PyObject *)&_PyExc_ ## EXCNAME;

#define MiddlingExtendsException(EXCBASE, EXCNAME, EXCSTORE, EXCDOC) \
static PyTypeObject _PyExc_ ## EXCNAME = { \
    PyObject_HEAD_INIT(NULL) \
    0, \
    EXC_MODULE_NAME # EXCNAME, \
    sizeof(Py ## EXCSTORE ## Object), \
    0, (destructor)BaseException_dealloc, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
    0, 0, 0, 0, 0, \
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE | Py_TPFLAGS_HAVE_GC, \
    PyDoc_STR(EXCDOC), (traverseproc)BaseException_traverse, \
    (inquiry)BaseException_clear, 0, 0, 0, 0, 0, 0, 0, &_ ## EXCBASE, \
    0, 0, 0, offsetof(Py ## EXCSTORE ## Object, dict), \
    (initproc)EXCSTORE ## _init, 0, EXCSTORE ## _new,\
}; \
PyObject *PyExc_ ## EXCNAME = (PyObject *)&_PyExc_ ## EXCNAME;

#define ComplexExtendsException(EXCBASE, EXCNAME, EXCSTORE, EXCDEALLOC, EXCMETHODS, EXCMEMBERS, EXCSTR, EXCDOC) \
static PyTypeObject _PyExc_ ## EXCNAME = { \
    PyObject_HEAD_INIT(NULL) \
    0, \
    EXC_MODULE_NAME # EXCNAME, \
    sizeof(Py ## EXCSTORE ## Object), 0, \
    (destructor)EXCSTORE ## _dealloc, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, \
    (reprfunc)EXCSTR, 0, 0, 0, \
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE | Py_TPFLAGS_HAVE_GC, \
    PyDoc_STR(EXCDOC), (traverseproc)EXCSTORE ## _traverse, \
    (inquiry)EXCSTORE ## _clear, 0, 0, 0, 0, EXCMETHODS, \
    EXCMEMBERS, 0, &_ ## EXCBASE, \
    0, 0, 0, offsetof(Py ## EXCSTORE ## Object, dict), \
    (initproc)EXCSTORE ## _init, 0, EXCSTORE ## _new,\
}; \
PyObject *PyExc_ ## EXCNAME = (PyObject *)&_PyExc_ ## EXCNAME;


/*
 *    Exception extends BaseException
 */
SimpleExtendsException(PyExc_BaseException, Exception,
                       "Common base class for all non-exit exceptions.")


/*
 *    StandardError extends Exception
 */
SimpleExtendsException(PyExc_Exception, StandardError, 
    "Base class for all standard Python exceptions that do not represent\n"
    "interpreter exiting.")


/*
 *    TypeError extends StandardError
 */
SimpleExtendsException(PyExc_StandardError, TypeError,
                       "Inappropriate argument type.")


/*
 *    StopIteration extends Exception
 */
SimpleExtendsException(PyExc_Exception, StopIteration,
                       "Signal the end from iterator.next().")


/*
 *    GeneratorExit extends Exception
 */
SimpleExtendsException(PyExc_Exception, GeneratorExit,
                       "Request that a generator exit.")


/*
 *    SystemExit extends BaseException
 */
static PyObject *
SystemExit_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    PySystemExitObject *self;

    self = (PySystemExitObject *)BaseException_new(type, args, kwds);
    if (!self)
        return NULL;

    MAKE_IT_NONE(self->code);

    return (PyObject *)self;
}

static int
SystemExit_init(PySystemExitObject *self, PyObject *args, PyObject *kwds)
{
    Py_ssize_t size = PyTuple_GET_SIZE(args);

    if (BaseException_init((PyBaseExceptionObject *)self, args, kwds) == -1)
        return -1;

    Py_DECREF(self->code);
    if (size == 1)
        self->code = PyTuple_GET_ITEM(args, 0);
    else if (size > 1)
        self->code = args;
    Py_INCREF(self->code);
    return 0;
}

int
SystemExit_clear(PySystemExitObject *self)
{
    Py_CLEAR(self->code);
    return BaseException_clear((PyBaseExceptionObject *)self);
}

static void
SystemExit_dealloc(PySystemExitObject *self)
{
    SystemExit_clear(self);
    self->ob_type->tp_free((PyObject *)self);
}

int
SystemExit_traverse(PySystemExitObject *self, visitproc visit, void *arg)
{
    Py_VISIT(self->code);
    return BaseException_traverse((PyBaseExceptionObject *)self, visit, arg);
}

static PyMemberDef SystemExit_members[] = {
    {"message", T_OBJECT, offsetof(PySystemExitObject, message), 0,
        PyDoc_STR("exception message")},
    {"code", T_OBJECT, offsetof(PySystemExitObject, code), 0,
        PyDoc_STR("exception code")},
    {NULL}  /* Sentinel */
};

ComplexExtendsException(PyExc_BaseException, SystemExit, SystemExit,
                        SystemExit_dealloc, 0, SystemExit_members, 0,
                        "Request to exit from the interpreter.") 

/*
 *    KeyboardInterrupt extends BaseException
 */
SimpleExtendsException(PyExc_BaseException, KeyboardInterrupt,
                       "Program interrupted by user.")


/*
 *    ImportError extends StandardError
 */
SimpleExtendsException(PyExc_StandardError, ImportError,
          "Import can't find module, or can't find name in module.")


/*
 *    EnvironmentError extends StandardError
 */

static PyObject *
EnvironmentError_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    PyEnvironmentErrorObject *self = NULL;

    self = (PyEnvironmentErrorObject *)BaseException_new(type, args, kwds);
    if (!self)
        return NULL;

    self->myerrno = Py_None;
    Py_INCREF(Py_None);
    self->strerror = Py_None;
    Py_INCREF(Py_None);
    self->filename = Py_None;
    Py_INCREF(Py_None);

    return (PyObject *)self;
}

/* Where a function has a single filename, such as open() or some
 * of the os module functions, PyErr_SetFromErrnoWithFilename() is
 * called, giving a third argument which is the filename.  But, so
 * that old code using in-place unpacking doesn't break, e.g.:
 *
 * except IOError, (errno, strerror):
 *
 * we hack args so that it only contains two items.  This also
 * means we need our own __str__() which prints out the filename
 * when it was supplied.
 */
static int
EnvironmentError_init(PyEnvironmentErrorObject *self, PyObject *args,
    PyObject *kwds)
{
    PyObject *myerrno = NULL, *strerror = NULL, *filename = NULL;
    PyObject *subslice = NULL;

    if (BaseException_init((PyBaseExceptionObject *)self, args, kwds) == -1)
        return -1;

    if (PyTuple_GET_SIZE(args) <= 1) {
        return 0;
    }
    
    if (!PyArg_UnpackTuple(args, "EnvironmentError", 2, 3, 
                           &myerrno, &strerror, &filename)) {
        return -1;
    }
    Py_DECREF(self->myerrno);       /* replacing */
    self->myerrno = myerrno;
    Py_INCREF(self->myerrno);

    Py_DECREF(self->strerror);      /* replacing */
    self->strerror = strerror;
    Py_INCREF(self->strerror);

    /* self->filename will remain Py_None otherwise */
    if (filename != NULL) {
        Py_DECREF(self->filename);      /* replacing */
        self->filename = filename;
        Py_INCREF(self->filename);

        subslice = PyTuple_GetSlice(args, 0, 2);
        if (!subslice)
            return -1;

        Py_DECREF(self->args);  /* replacing args */
        self->args = subslice;
    }
    return 0;
}

int
EnvironmentError_clear(PyEnvironmentErrorObject *self)
{
    Py_CLEAR(self->myerrno);
    Py_CLEAR(self->strerror);
    Py_CLEAR(self->filename);
    return BaseException_clear((PyBaseExceptionObject *)self);
}

static void
EnvironmentError_dealloc(PyEnvironmentErrorObject *self)
{
    EnvironmentError_clear(self);
    self->ob_type->tp_free((PyObject *)self);
}

int
EnvironmentError_traverse(PyEnvironmentErrorObject *self, visitproc visit,
        void *arg)
{
    Py_VISIT(self->myerrno);
    Py_VISIT(self->strerror);
    Py_VISIT(self->filename);
    return BaseException_traverse((PyBaseExceptionObject *)self, visit, arg);
}

static PyObject *
EnvironmentError_str(PyEnvironmentErrorObject *self)
{
    PyObject *rtnval = NULL;

    if (self->filename != Py_None) {
        PyObject *fmt = PyString_FromString("[Errno %s] %s: %s");
        PyObject *repr = PyObject_Repr(self->filename);
        PyObject *tuple = PyTuple_New(3);

        if (!fmt || !repr || !tuple) {
            Py_XDECREF(fmt);
            Py_XDECREF(repr);
            Py_XDECREF(tuple);
            return NULL;
        }
        Py_INCREF(self->myerrno);
        PyTuple_SET_ITEM(tuple, 0, self->myerrno);
        Py_INCREF(self->strerror);
        PyTuple_SET_ITEM(tuple, 1, self->strerror);
        Py_INCREF(repr);
        PyTuple_SET_ITEM(tuple, 2, repr);

        rtnval = PyString_Format(fmt, tuple);

        Py_DECREF(fmt);
        Py_DECREF(tuple);
    }
    else if (PyObject_IsTrue(self->myerrno) &&
            PyObject_IsTrue(self->strerror)) {
        PyObject *fmt = PyString_FromString("[Errno %s] %s");
        PyObject *tuple = PyTuple_New(2);

        if (!fmt || !tuple) {
            Py_XDECREF(fmt);
            Py_XDECREF(tuple);
            return NULL;
        }
        Py_INCREF(self->myerrno);
        PyTuple_SET_ITEM(tuple, 0, self->myerrno);
        Py_INCREF(self->strerror);
        PyTuple_SET_ITEM(tuple, 1, self->strerror);

        rtnval = PyString_Format(fmt, tuple);

        Py_DECREF(fmt);
        Py_DECREF(tuple);
    }
    else
        rtnval = BaseException_str((PyBaseExceptionObject *)self);

    return rtnval;
}

static PyMemberDef EnvironmentError_members[] = {
    {"message", T_OBJECT, offsetof(PyEnvironmentErrorObject, message), 0,
        PyDoc_STR("exception message")},
    {"errno", T_OBJECT, offsetof(PyEnvironmentErrorObject, myerrno), 0,
        PyDoc_STR("exception code")},
    {"strerror", T_OBJECT, offsetof(PyEnvironmentErrorObject, strerror), 0,
        PyDoc_STR("exception code")},
    {"filename", T_OBJECT, offsetof(PyEnvironmentErrorObject, filename), 0,
        PyDoc_STR("exception code")},
    {NULL}  /* Sentinel */
};


static PyObject *
EnvironmentError_reduce(PyEnvironmentErrorObject *self)
{
    PyObject *args = self->args;
    PyObject *res = NULL, *tmp;
    /* self->args is only the first two real arguments if there was a
     * file name given to EnvironmentError. */
    if (PyTuple_Check(args) && 
        PyTuple_GET_SIZE(args) == 2 &&
        self->filename != Py_None) {  

        args = PyTuple_New(3);
        if (!args) return NULL;
        
        tmp = PyTuple_GetItem(self->args, 0);
        if (!tmp) goto finish;
        Py_INCREF(tmp);
        PyTuple_SET_ITEM(args, 0, tmp);
        
        tmp = PyTuple_GetItem(self->args, 1);
        if (!tmp) goto finish;
        Py_INCREF(tmp);
        PyTuple_SET_ITEM(args, 1, tmp);

        Py_INCREF(self->filename);
        PyTuple_SET_ITEM(args, 2, self->filename);
    } else {
        Py_INCREF(args);
    }
    res = PyTuple_Pack(3, self->ob_type, args, self->dict);
  finish:
    Py_DECREF(args);
    return res;
}


static PyMethodDef EnvironmentError_methods[] = {
    {"__reduce__", (PyCFunction)EnvironmentError_reduce, METH_NOARGS},
    {NULL}
};

ComplexExtendsException(PyExc_StandardError, EnvironmentError,
                        EnvironmentError, EnvironmentError_dealloc,
                        EnvironmentError_methods, EnvironmentError_members,
                        EnvironmentError_str, 
                        "Base class for I/O related errors.")


/*
 *    IOError extends EnvironmentError
 */
MiddlingExtendsException(PyExc_EnvironmentError, IOError, 
                         EnvironmentError, "I/O operation failed.")


/*
 *    OSError extends EnvironmentError
 */
MiddlingExtendsException(PyExc_EnvironmentError, OSError,
                         EnvironmentError, "OS system call failed.")


/*
 *    WindowsError extends OSError
 */
#ifdef MS_WINDOWS
#include "errmap.h"

int
WindowsError_clear(PyWindowsErrorObject *self)
{
    Py_CLEAR(self->myerrno);
    Py_CLEAR(self->strerror);
    Py_CLEAR(self->filename);
    Py_CLEAR(self->winerror);
    return BaseException_clear((PyBaseExceptionObject *)self);
}

static void
WindowsError_dealloc(PyWindowsErrorObject *self)
{
    WindowsError_clear(self);
    self->ob_type->tp_free((PyObject *)self);
}

int
WindowsError_traverse(PyWindowsErrorObject *self, visitproc visit, void *arg)
{
    Py_VISIT(self->myerrno);
    Py_VISIT(self->strerror);
    Py_VISIT(self->filename);
    Py_VISIT(self->winerror);
    return BaseException_traverse((PyBaseExceptionObject *)self, visit, arg);
}

static PyObject *
WindowsError_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    PyObject *o_errcode = NULL;
    long errcode;
    PyWindowsErrorObject *self;
    long posix_errno;

    self = (PyWindowsErrorObject *)EnvironmentError_new(type, args, kwds);
    if (!self)
        return NULL;

    if (self->myerrno == Py_None) {
        self->winerror = self->myerrno;
        Py_INCREF(self->winerror);
        return (PyObject *)self;
    }

    /* Set errno to the POSIX errno, and winerror to the Win32
       error code. */
    errcode = PyInt_AsLong(self->myerrno);
    if (errcode == -1 && PyErr_Occurred()) {
        if (PyErr_ExceptionMatches(PyExc_TypeError))
            /* give a clearer error message */
            PyErr_SetString(PyExc_TypeError, "errno has to be an integer");
        goto failed;
    }
    posix_errno = winerror_to_errno(errcode);

    self->winerror = self->myerrno;

    o_errcode = PyInt_FromLong(posix_errno);
    if (!o_errcode)
        goto failed;

    self->myerrno = o_errcode;

    return (PyObject *)self;
failed:
    /* Could not set errno. */
    Py_DECREF(self);
    return NULL;
}

static int
WindowsError_init(PyWindowsErrorObject *self, PyObject *args, PyObject *kwds)
{
    PyObject *o_errcode = NULL;
    long errcode;
    long posix_errno;

    if (EnvironmentError_init((PyEnvironmentErrorObject *)self, args, kwds)
            == -1)
        return -1;

    if (self->myerrno == Py_None) {
        Py_DECREF(self->winerror);
        self->winerror = self->myerrno;
        Py_INCREF(self->winerror);
        return 0;
    }

    /* Set errno to the POSIX errno, and winerror to the Win32
       error code. */
    errcode = PyInt_AsLong(self->myerrno);
    if (errcode == -1 && PyErr_Occurred())
        return -1;
    posix_errno = winerror_to_errno(errcode);

    Py_DECREF(self->winerror);
    self->winerror = self->myerrno;

    o_errcode = PyInt_FromLong(posix_errno);
    if (!o_errcode)
        return -1;

    self->myerrno = o_errcode;

    return 0;
}


static PyObject *
WindowsError_str(PyWindowsErrorObject *self)
{
    PyObject *repr = NULL;
    PyObject *fmt = NULL;
    PyObject *tuple = NULL;
    PyObject *rtnval = NULL;

    if (self->filename != Py_None) {
        fmt = PyString_FromString("[Error %s] %s: %s");
        repr = PyObject_Repr(self->filename);
        if (!fmt || !repr)
            goto finally;

        tuple = PyTuple_Pack(3, self->myerrno, self->strerror, repr);
        if (!tuple)
            goto finally;

        rtnval = PyString_Format(fmt, tuple);
        Py_DECREF(tuple);
    }
    else if (PyObject_IsTrue(self->myerrno) &&
            PyObject_IsTrue(self->strerror)) {
        fmt = PyString_FromString("[Error %s] %s");
        if (!fmt)
            goto finally;

        tuple = PyTuple_Pack(2, self->myerrno, self->strerror);
        if (!tuple)
            goto finally;

        rtnval = PyString_Format(fmt, tuple);
        Py_DECREF(tuple);
    }
    else
    rtnval = EnvironmentError_str((PyEnvironmentErrorObject *)self);

  finally:
    Py_XDECREF(repr);
    Py_XDECREF(fmt);
    Py_XDECREF(tuple);
    return rtnval;
}

static PyMemberDef WindowsError_members[] = {
    {"message", T_OBJECT, offsetof(PyWindowsErrorObject, message), 0,
        PyDoc_STR("exception message")},
    {"errno", T_OBJECT, offsetof(PyWindowsErrorObject, myerrno), 0,
        PyDoc_STR("exception code")},
    {"strerror", T_OBJECT, offsetof(PyWindowsErrorObject, strerror), 0,
        PyDoc_STR("exception code")},
    {"filename", T_OBJECT, offsetof(PyWindowsErrorObject, filename), 0,
        PyDoc_STR("exception code")},
    {"winerror", T_OBJECT, offsetof(PyWindowsErrorObject, winerror), 0,
        PyDoc_STR("windows exception code")},
    {NULL}  /* Sentinel */
};

ComplexExtendsException(PyExc_OSError,
                        WindowsError,
                        WindowsError,
                        WindowsError_dealloc,
                        0,
                        WindowsError_members,
                        WindowsError_str,
                        "MS-Windows OS system call failed.")

#endif /* MS_WINDOWS */


/*
 *    VMSError extends OSError (I think)
 */
#ifdef __VMS
MiddlingExtendsException(PyExc_OSError, VMSError, EnvironmentError,
                         "OpenVMS OS system call failed.")
#endif


/*
 *    EOFError extends StandardError
 */
SimpleExtendsException(PyExc_StandardError, EOFError,
                       "Read beyond end of file.")


/*
 *    RuntimeError extends StandardError
 */
SimpleExtendsException(PyExc_StandardError, RuntimeError,
                       "Unspecified run-time error.")


/*
 *    NotImplementedError extends RuntimeError
 */
SimpleExtendsException(PyExc_RuntimeError, NotImplementedError,
                       "Method or function hasn't been implemented yet.")

/*
 *    NameError extends StandardError
 */
SimpleExtendsException(PyExc_StandardError, NameError,
                       "Name not found globally.")

/*
 *    UnboundLocalError extends NameError
 */
SimpleExtendsException(PyExc_NameError, UnboundLocalError,
                       "Local name referenced but not bound to a value.")

/*
 *    AttributeError extends StandardError
 */
SimpleExtendsException(PyExc_StandardError, AttributeError,
                       "Attribute not found.")


/*
 *    SyntaxError extends StandardError
 */
static PyObject *
SyntaxError_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    PySyntaxErrorObject *self = NULL;

    self = (PySyntaxErrorObject *)BaseException_new(type, args, kwds);
    if (!self)
        return NULL;

    MAKE_IT_NONE(self->msg)
    MAKE_IT_NONE(self->filename)
    MAKE_IT_NONE(self->lineno)
    MAKE_IT_NONE(self->offset)
    MAKE_IT_NONE(self->text)

    /* this is always None - yes, I know it doesn't seem to be used
       anywhere, but it was in the previous implementation */
    MAKE_IT_NONE(self->print_file_and_line)

    return (PyObject *)self;
}

static int
SyntaxError_init(PySyntaxErrorObject *self, PyObject *args, PyObject *kwds)
{
    PyObject *info = NULL;
    Py_ssize_t lenargs = PyTuple_GET_SIZE(args);

    if (BaseException_init((PyBaseExceptionObject *)self, args, kwds) == -1)
        return -1;

    if (lenargs >= 1) {
        Py_DECREF(self->msg);
        self->msg = PyTuple_GET_ITEM(args, 0);
        Py_INCREF(self->msg);
    }
    if (lenargs == 2) {
        info = PyTuple_GET_ITEM(args, 1);
        info = PySequence_Tuple(info);
        if (!info) return -1;

        Py_DECREF(self->filename);
        self->filename = PyTuple_GET_ITEM(info, 0);
        Py_INCREF(self->filename);

        Py_DECREF(self->lineno);
        self->lineno = PyTuple_GET_ITEM(info, 1);
        Py_INCREF(self->lineno);

        Py_DECREF(self->offset);
        self->offset = PyTuple_GET_ITEM(info, 2);
        Py_INCREF(self->offset);

        Py_DECREF(self->text);
        self->text = PyTuple_GET_ITEM(info, 3);
        Py_INCREF(self->text);
    }
    return 0;
}

int
SyntaxError_clear(PySyntaxErrorObject *self)
{
    Py_CLEAR(self->msg);
    Py_CLEAR(self->filename);
    Py_CLEAR(self->lineno);
    Py_CLEAR(self->offset);
    Py_CLEAR(self->text);
    Py_CLEAR(self->print_file_and_line);
    return BaseException_clear((PyBaseExceptionObject *)self);
}

static void
SyntaxError_dealloc(PySyntaxErrorObject *self)
{
    SyntaxError_clear(self);
    self->ob_type->tp_free((PyObject *)self);
}

int
SyntaxError_traverse(PySyntaxErrorObject *self, visitproc visit, void *arg)
{
    Py_VISIT(self->msg);
    Py_VISIT(self->filename);
    Py_VISIT(self->lineno);
    Py_VISIT(self->offset);
    Py_VISIT(self->text);
    Py_VISIT(self->print_file_and_line);
    return BaseException_traverse((PyBaseExceptionObject *)self, visit, arg);
}

/* This is called "my_basename" instead of just "basename" to avoid name
   conflicts with glibc; basename is already prototyped if _GNU_SOURCE is
   defined, and Python does define that. */
static char *
my_basename(char *name)
{
    char *cp = name;
    char *result = name;

    if (name == NULL)
        return "???";
    while (*cp != '\0') {
        if (*cp == SEP)
            result = cp + 1;
        ++cp;
    }
    return result;
}


static PyObject *
SyntaxError_str(PySyntaxErrorObject *self)
{
    PyObject *str;
    PyObject *result;

    str = PyObject_Str(self->msg);
    result = str;

    /* XXX -- do all the additional formatting with filename and
       lineno here */

    if (str != NULL && PyString_Check(str)) {
        int have_filename = 0;
        int have_lineno = 0;
        char *buffer = NULL;

        have_filename = (self->filename != NULL) && 
            PyString_Check(self->filename);
        have_lineno = (self->lineno != NULL) && PyInt_Check(self->lineno);

        if (have_filename || have_lineno) {
            Py_ssize_t bufsize = PyString_GET_SIZE(str) + 64;
            if (have_filename)
                bufsize += PyString_GET_SIZE(self->filename);

            buffer = (char *)PyMem_MALLOC(bufsize);
            if (buffer != NULL) {
                if (have_filename && have_lineno)
                    PyOS_snprintf(buffer, bufsize, "%s (%s, line %ld)",
                        PyString_AS_STRING(str),
                        my_basename(PyString_AS_STRING(self->filename)),
                        PyInt_AsLong(self->lineno));
                else if (have_filename)
                    PyOS_snprintf(buffer, bufsize, "%s (%s)",
                        PyString_AS_STRING(str),
                        my_basename(PyString_AS_STRING(self->filename)));
                else if (have_lineno)
                    PyOS_snprintf(buffer, bufsize, "%s (line %ld)",
                        PyString_AS_STRING(str),
                        PyInt_AsLong(self->lineno));

                result = PyString_FromString(buffer);
                PyMem_FREE(buffer);

                if (result == NULL)
                    result = str;
                else
                    Py_DECREF(str);
            }
        }
    }
    return result;
}

static PyMemberDef SyntaxError_members[] = {
    {"message", T_OBJECT, offsetof(PySyntaxErrorObject, message), 0,
        PyDoc_STR("exception message")},
    {"msg", T_OBJECT, offsetof(PySyntaxErrorObject, msg), 0,
        PyDoc_STR("exception msg")},
    {"filename", T_OBJECT, offsetof(PySyntaxErrorObject, filename), 0,
        PyDoc_STR("exception filename")},
    {"lineno", T_OBJECT, offsetof(PySyntaxErrorObject, lineno), 0,
        PyDoc_STR("exception lineno")},
    {"offset", T_OBJECT, offsetof(PySyntaxErrorObject, offset), 0,
        PyDoc_STR("exception offset")},
    {"text", T_OBJECT, offsetof(PySyntaxErrorObject, text), 0,
        PyDoc_STR("exception text")},
    {"print_file_and_line", T_OBJECT,
        offsetof(PySyntaxErrorObject, print_file_and_line), 0,
        PyDoc_STR("exception print_file_and_line")},
    {NULL}  /* Sentinel */
};

ComplexExtendsException(PyExc_StandardError, SyntaxError, SyntaxError,
                        SyntaxError_dealloc, 0, SyntaxError_members,
                        SyntaxError_str, "Invalid syntax.")


/*
 *    IndentationError extends SyntaxError
 */
MiddlingExtendsException(PyExc_SyntaxError, IndentationError, SyntaxError,
                         "Improper indentation.")


/*
 *    TabError extends IndentationError
 */
MiddlingExtendsException(PyExc_IndentationError, TabError, SyntaxError,
                         "Improper mixture of spaces and tabs.")


/*
 *    LookupError extends StandardError
 */
SimpleExtendsException(PyExc_StandardError, LookupError,
                       "Base class for lookup errors.")


/*
 *    IndexError extends LookupError
 */
SimpleExtendsException(PyExc_LookupError, IndexError,
                       "Sequence index out of range.")


/*
 *    KeyError extends LookupError
 */
static PyObject *
KeyError_str(PyBaseExceptionObject *self)
{
    /* If args is a tuple of exactly one item, apply repr to args[0].
       This is done so that e.g. the exception raised by {}[''] prints
         KeyError: ''
       rather than the confusing
         KeyError
       alone.  The downside is that if KeyError is raised with an explanatory
       string, that string will be displayed in quotes.  Too bad.
       If args is anything else, use the default BaseException__str__().
    */
    if (PyTuple_Check(self->args) && PyTuple_GET_SIZE(self->args) == 1) {
        PyObject *key = PyTuple_GET_ITEM(self->args, 0);
        return PyObject_Repr(key);
    }
    return BaseException_str(self);
}

ComplexExtendsException(PyExc_LookupError, KeyError, BaseException,
                        0, 0, 0, KeyError_str, "Mapping key not found.")


/*
 *    ValueError extends StandardError
 */
SimpleExtendsException(PyExc_StandardError, ValueError,
                       "Inappropriate argument value (of correct type).")

/*
 *    UnicodeError extends ValueError
 */

SimpleExtendsException(PyExc_ValueError, UnicodeError,
                       "Unicode related error.")

#ifdef Py_USING_UNICODE
static int
get_int(PyObject *attr, Py_ssize_t *value, const char *name)
{
    if (!attr) {
        PyErr_Format(PyExc_TypeError, "%.200s attribute not set", name);
        return -1;
    }

    if (PyInt_Check(attr)) {
        *value = PyInt_AS_LONG(attr);
    } else if (PyLong_Check(attr)) {
        *value = _PyLong_AsSsize_t(attr);
        if (*value == -1 && PyErr_Occurred())
            return -1;
    } else {
        PyErr_Format(PyExc_TypeError, "%.200s attribute must be int", name);
        return -1;
    }
    return 0;
}

static int
set_ssize_t(PyObject **attr, Py_ssize_t value)
{
    PyObject *obj = PyInt_FromSsize_t(value);
    if (!obj)
        return -1;
    Py_XDECREF(*attr);
    *attr = obj;
    return 0;
}

static PyObject *
get_string(PyObject *attr, const char *name)
{
    if (!attr) {
        PyErr_Format(PyExc_TypeError, "%.200s attribute not set", name);
        return NULL;
    }

    if (!PyString_Check(attr)) {
        PyErr_Format(PyExc_TypeError, "%.200s attribute must be str", name);
        return NULL;
    }
    Py_INCREF(attr);
    return attr;
}


static int
set_string(PyObject **attr, const char *value)
{
    PyObject *obj = PyString_FromString(value);
    if (!obj)
        return -1;
    Py_XDECREF(*attr);
    *attr = obj;
    return 0;
}


static PyObject *
get_unicode(PyObject *attr, const char *name)
{
    if (!attr) {
        PyErr_Format(PyExc_TypeError, "%.200s attribute not set", name);
        return NULL;
    }

    if (!PyUnicode_Check(attr)) {
        PyErr_Format(PyExc_TypeError,
                     "%.200s attribute must be unicode", name);
        return NULL;
    }
    Py_INCREF(attr);
    return attr;
}

PyObject *
PyUnicodeEncodeError_GetEncoding(PyObject *exc)
{
    return get_string(((PyUnicodeErrorObject *)exc)->encoding, "encoding");
}

PyObject *
PyUnicodeDecodeError_GetEncoding(PyObject *exc)
{
    return get_string(((PyUnicodeErrorObject *)exc)->encoding, "encoding");
}

PyObject *
PyUnicodeEncodeError_GetObject(PyObject *exc)
{
    return get_unicode(((PyUnicodeErrorObject *)exc)->object, "object");
}

PyObject *
PyUnicodeDecodeError_GetObject(PyObject *exc)
{
    return get_string(((PyUnicodeErrorObject *)exc)->object, "object");
}

PyObject *
PyUnicodeTranslateError_GetObject(PyObject *exc)
{
    return get_unicode(((PyUnicodeErrorObject *)exc)->object, "object");
}

int
PyUnicodeEncodeError_GetStart(PyObject *exc, Py_ssize_t *start)
{
    if (!get_int(((PyUnicodeErrorObject *)exc)->start, start, "start")) {
        Py_ssize_t size;
        PyObject *obj = get_unicode(((PyUnicodeErrorObject *)exc)->object,
                                    "object");
        if (!obj) return -1;
        size = PyUnicode_GET_SIZE(obj);
        if (*start<0)
            *start = 0; /*XXX check for values <0*/
        if (*start>=size)
            *start = size-1;
        return 0;
    }
    return -1;
}


int
PyUnicodeDecodeError_GetStart(PyObject *exc, Py_ssize_t *start)
{
    if (!get_int(((PyUnicodeErrorObject *)exc)->start, start, "start")) {
        Py_ssize_t size;
        PyObject *obj = get_string(((PyUnicodeErrorObject *)exc)->object,
                                   "object");
        if (!obj) return -1;
        size = PyString_GET_SIZE(obj);
        if (*start<0)
            *start = 0;
        if (*start>=size)
            *start = size-1;
        return 0;
    }
    return -1;
}


int
PyUnicodeTranslateError_GetStart(PyObject *exc, Py_ssize_t *start)
{
    return PyUnicodeEncodeError_GetStart(exc, start);
}


int
PyUnicodeEncodeError_SetStart(PyObject *exc, Py_ssize_t start)
{
    return set_ssize_t(&((PyUnicodeErrorObject *)exc)->start, start);
}


int
PyUnicodeDecodeError_SetStart(PyObject *exc, Py_ssize_t start)
{
    return set_ssize_t(&((PyUnicodeErrorObject *)exc)->start, start);
}


int
PyUnicodeTranslateError_SetStart(PyObject *exc, Py_ssize_t start)
{
    return set_ssize_t(&((PyUnicodeErrorObject *)exc)->start, start);
}


int
PyUnicodeEncodeError_GetEnd(PyObject *exc, Py_ssize_t *end)
{
    if (!get_int(((PyUnicodeErrorObject *)exc)->end, end, "end")) {
        Py_ssize_t size;
        PyObject *obj = get_unicode(((PyUnicodeErrorObject *)exc)->object,
                                    "object");
        if (!obj) return -1;
        size = PyUnicode_GET_SIZE(obj);
        if (*end<1)
            *end = 1;
        if (*end>size)
            *end = size;
        return 0;
    }
    return -1;
}


int
PyUnicodeDecodeError_GetEnd(PyObject *exc, Py_ssize_t *end)
{
    if (!get_int(((PyUnicodeErrorObject *)exc)->end, end, "end")) {
        Py_ssize_t size;
        PyObject *obj = get_string(((PyUnicodeErrorObject *)exc)->object,
                                   "object");
        if (!obj) return -1;
        size = PyString_GET_SIZE(obj);
        if (*end<1)
            *end = 1;
        if (*end>size)
            *end = size;
        return 0;
    }
    return -1;
}


int
PyUnicodeTranslateError_GetEnd(PyObject *exc, Py_ssize_t *start)
{
    return PyUnicodeEncodeError_GetEnd(exc, start);
}


int
PyUnicodeEncodeError_SetEnd(PyObject *exc, Py_ssize_t end)
{
    return set_ssize_t(&((PyUnicodeErrorObject *)exc)->end, end);
}


int
PyUnicodeDecodeError_SetEnd(PyObject *exc, Py_ssize_t end)
{
    return set_ssize_t(&((PyUnicodeErrorObject *)exc)->end, end);
}


int
PyUnicodeTranslateError_SetEnd(PyObject *exc, Py_ssize_t end)
{
    return set_ssize_t(&((PyUnicodeErrorObject *)exc)->end, end);
}

PyObject *
PyUnicodeEncodeError_GetReason(PyObject *exc)
{
    return get_string(((PyUnicodeErrorObject *)exc)->reason, "reason");
}


PyObject *
PyUnicodeDecodeError_GetReason(PyObject *exc)
{
    return get_string(((PyUnicodeErrorObject *)exc)->reason, "reason");
}


PyObject *
PyUnicodeTranslateError_GetReason(PyObject *exc)
{
    return get_string(((PyUnicodeErrorObject *)exc)->reason, "reason");
}


int
PyUnicodeEncodeError_SetReason(PyObject *exc, const char *reason)
{
    return set_string(&((PyUnicodeErrorObject *)exc)->reason, reason);
}


int
PyUnicodeDecodeError_SetReason(PyObject *exc, const char *reason)
{
    return set_string(&((PyUnicodeErrorObject *)exc)->reason, reason);
}


int
PyUnicodeTranslateError_SetReason(PyObject *exc, const char *reason)
{
    return set_string(&((PyUnicodeErrorObject *)exc)->reason, reason);
}


static PyObject *
UnicodeError_new(PyTypeObject *type, PyObject *args, PyObject *kwds,
                 PyTypeObject *objecttype)
{
    PyUnicodeErrorObject *self;

    self = (PyUnicodeErrorObject *)BaseException_new(type, args, kwds);
    if (!self)
        return NULL;

    MAKE_IT_NONE(self->encoding);
    MAKE_IT_NONE(self->object);
    MAKE_IT_NONE(self->start);
    MAKE_IT_NONE(self->end);
    MAKE_IT_NONE(self->reason);

    return (PyObject *)self;
}

static int
UnicodeError_init(PyUnicodeErrorObject *self, PyObject *args, PyObject *kwds,
                  PyTypeObject *objecttype)
{
    if (!PyArg_ParseTuple(args, "O!O!O!O!O!",
        &PyString_Type, &self->encoding,
        objecttype, &self->object,
        &PyInt_Type, &self->start,
        &PyInt_Type, &self->end,
        &PyString_Type, &self->reason)) {
        self->encoding = self->object = self->start = self->end = 
            self->reason = NULL;
        return -1;
    }

    Py_INCREF(self->encoding);
    Py_INCREF(self->object);
    Py_INCREF(self->start);
    Py_INCREF(self->end);
    Py_INCREF(self->reason);

    return 0;
}

int
UnicodeError_clear(PyUnicodeErrorObject *self)
{
    Py_CLEAR(self->encoding);
    Py_CLEAR(self->object);
    Py_CLEAR(self->start);
    Py_CLEAR(self->end);
    Py_CLEAR(self->reason);
    return BaseException_clear((PyBaseExceptionObject *)self);
}

static void
UnicodeError_dealloc(PyUnicodeErrorObject *self)
{
    UnicodeError_clear(self);
    self->ob_type->tp_free((PyObject *)self);
}

int
UnicodeError_traverse(PyUnicodeErrorObject *self, visitproc visit, void *arg)
{
    Py_VISIT(self->encoding);
    Py_VISIT(self->object);
    Py_VISIT(self->start);
    Py_VISIT(self->end);
    Py_VISIT(self->reason);
    return BaseException_traverse((PyBaseExceptionObject *)self, visit, arg);
}

static PyMemberDef UnicodeError_members[] = {
    {"message", T_OBJECT, offsetof(PyUnicodeErrorObject, message), 0,
        PyDoc_STR("exception message")},
    {"encoding", T_OBJECT, offsetof(PyUnicodeErrorObject, encoding), 0,
        PyDoc_STR("exception encoding")},
    {"object", T_OBJECT, offsetof(PyUnicodeErrorObject, object), 0,
        PyDoc_STR("exception object")},
    {"start", T_OBJECT, offsetof(PyUnicodeErrorObject, start), 0,
        PyDoc_STR("exception start")},
    {"end", T_OBJECT, offsetof(PyUnicodeErrorObject, end), 0,
        PyDoc_STR("exception end")},
    {"reason", T_OBJECT, offsetof(PyUnicodeErrorObject, reason), 0,
        PyDoc_STR("exception reason")},
    {NULL}  /* Sentinel */
};


/*
 *    UnicodeEncodeError extends UnicodeError
 */
static PyObject *
UnicodeEncodeError_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    return UnicodeError_new(type, args, kwds, &PyUnicode_Type);
}

static int
UnicodeEncodeError_init(PyObject *self, PyObject *args, PyObject *kwds)
{
    if (BaseException_init((PyBaseExceptionObject *)self, args, kwds) == -1)
        return -1;
    return UnicodeError_init((PyUnicodeErrorObject *)self, args,
                             kwds, &PyUnicode_Type);
}

static PyObject *
UnicodeEncodeError_str(PyObject *self)
{
    Py_ssize_t start;
    Py_ssize_t end;

    if (PyUnicodeEncodeError_GetStart(self, &start))
    return NULL;

    if (PyUnicodeEncodeError_GetEnd(self, &end))
    return NULL;

    if (end==start+1) {
    int badchar = (int)PyUnicode_AS_UNICODE(((PyUnicodeErrorObject *)self)->object)[start];
    char badchar_str[20];
    if (badchar <= 0xff)
        PyOS_snprintf(badchar_str, sizeof(badchar_str), "x%02x", badchar);
    else if (badchar <= 0xffff)
        PyOS_snprintf(badchar_str, sizeof(badchar_str), "u%04x", badchar);
    else
        PyOS_snprintf(badchar_str, sizeof(badchar_str), "U%08x", badchar);
    return PyString_FromFormat(
        "'%.400s' codec can't encode character u'\\%s' in position %zd: %.400s",
        PyString_AS_STRING(((PyUnicodeErrorObject *)self)->encoding),
        badchar_str,
        start,
        PyString_AS_STRING(((PyUnicodeErrorObject *)self)->reason)
    );
    }
    return PyString_FromFormat(
        "'%.400s' codec can't encode characters in position %zd-%zd: %.400s",
        PyString_AS_STRING(((PyUnicodeErrorObject *)self)->encoding),
        start,
        (end-1),
        PyString_AS_STRING(((PyUnicodeErrorObject *)self)->reason)
    );
}

static PyTypeObject _PyExc_UnicodeEncodeError = {
    PyObject_HEAD_INIT(NULL)
    0,
    "UnicodeEncodeError",
    sizeof(PyUnicodeErrorObject), 0,
    (destructor)UnicodeError_dealloc, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    (reprfunc)UnicodeEncodeError_str, 0, 0, 0,
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE | Py_TPFLAGS_HAVE_GC,
    PyDoc_STR("Unicode encoding error."), (traverseproc)BaseException_traverse,
    (inquiry)BaseException_clear, 0, 0, 0, 0, 0, UnicodeError_members,
    0, &_PyExc_UnicodeError, 0, 0, 0, offsetof(PyUnicodeErrorObject, dict),
    (initproc)UnicodeEncodeError_init, 0, UnicodeEncodeError_new,
};
PyObject *PyExc_UnicodeEncodeError = (PyObject *)&_PyExc_UnicodeEncodeError;

PyObject *
PyUnicodeEncodeError_Create(
    const char *encoding, const Py_UNICODE *object, Py_ssize_t length,
    Py_ssize_t start, Py_ssize_t end, const char *reason)
{
    return PyObject_CallFunction(PyExc_UnicodeEncodeError, "su#nns",
    encoding, object, length, start, end, reason);
}


/*
 *    UnicodeDecodeError extends UnicodeError
 */
static PyObject *
UnicodeDecodeError_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    return UnicodeError_new(type, args, kwds, &PyString_Type);
}

static int
UnicodeDecodeError_init(PyObject *self, PyObject *args, PyObject *kwds)
{
    if (BaseException_init((PyBaseExceptionObject *)self, args, kwds) == -1)
        return -1;
    return UnicodeError_init((PyUnicodeErrorObject *)self, args,
                             kwds, &PyString_Type);
}

static PyObject *
UnicodeDecodeError_str(PyObject *self)
{
    Py_ssize_t start;
    Py_ssize_t end;

    if (PyUnicodeDecodeError_GetStart(self, &start))
    return NULL;

    if (PyUnicodeDecodeError_GetEnd(self, &end))
    return NULL;

    if (end==start+1) {
    /* FromFormat does not support %02x, so format that separately */
    char byte[4];
    PyOS_snprintf(byte, sizeof(byte), "%02x", 
              ((int)PyString_AS_STRING(((PyUnicodeErrorObject *)self)->object)[start])&0xff);
    return PyString_FromFormat(                     
        "'%.400s' codec can't decode byte 0x%s in position %zd: %.400s",
        PyString_AS_STRING(((PyUnicodeErrorObject *)self)->encoding),
        byte,
        start,
        PyString_AS_STRING(((PyUnicodeErrorObject *)self)->reason)
    );
    }
    return PyString_FromFormat(
        "'%.400s' codec can't decode bytes in position %zd-%zd: %.400s",
        PyString_AS_STRING(((PyUnicodeErrorObject *)self)->encoding),
        start,
        (end-1),
        PyString_AS_STRING(((PyUnicodeErrorObject *)self)->reason)
    );
}

static PyTypeObject _PyExc_UnicodeDecodeError = {
    PyObject_HEAD_INIT(NULL)
    0,
    EXC_MODULE_NAME "UnicodeDecodeError",
    sizeof(PyUnicodeErrorObject), 0,
    (destructor)UnicodeError_dealloc, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    (reprfunc)UnicodeDecodeError_str, 0, 0, 0,
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE | Py_TPFLAGS_HAVE_GC,
    PyDoc_STR("Unicode decoding error."), (traverseproc)BaseException_traverse,
    (inquiry)BaseException_clear, 0, 0, 0, 0, 0, UnicodeError_members,
    0, &_PyExc_UnicodeError, 0, 0, 0, offsetof(PyUnicodeErrorObject, dict),
    (initproc)UnicodeDecodeError_init, 0, UnicodeDecodeError_new,
};
PyObject *PyExc_UnicodeDecodeError = (PyObject *)&_PyExc_UnicodeDecodeError;

PyObject *
PyUnicodeDecodeError_Create(
    const char *encoding, const char *object, Py_ssize_t length,
    Py_ssize_t start, Py_ssize_t end, const char *reason)
{
    assert(length < INT_MAX);
    assert(start < INT_MAX);
    assert(end < INT_MAX);
    return PyObject_CallFunction(PyExc_UnicodeDecodeError, "ss#nns",
    encoding, object, length, start, end, reason);
}


/*
 *    UnicodeTranslateError extends UnicodeError
 */
static PyObject *
UnicodeTranslateError_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    PyUnicodeErrorObject *self = NULL;

    self = (PyUnicodeErrorObject *)BaseException_new(type, args, kwds);
    if (!self)
        return NULL;

    MAKE_IT_NONE(self->encoding);
    MAKE_IT_NONE(self->object);
    MAKE_IT_NONE(self->start);
    MAKE_IT_NONE(self->end);
    MAKE_IT_NONE(self->reason);

    return (PyObject *)self;
}

static int
UnicodeTranslateError_init(PyUnicodeErrorObject *self, PyObject *args,
                           PyObject *kwds)
{
    if (BaseException_init((PyBaseExceptionObject *)self, args, kwds) == -1)
        return -1;

    Py_CLEAR(self->object);
    Py_CLEAR(self->start);
    Py_CLEAR(self->end);
    Py_CLEAR(self->reason);

    if (!PyArg_ParseTuple(args, "O!O!O!O!",
        &PyUnicode_Type, &self->object,
        &PyInt_Type, &self->start,
        &PyInt_Type, &self->end,
        &PyString_Type, &self->reason)) {
        self->object = self->start = self->end = self->reason = NULL;
        return -1;
    }
    
    Py_INCREF(self->object);
    Py_INCREF(self->start);
    Py_INCREF(self->end);
    Py_INCREF(self->reason);

    return 0;
}


static PyObject *
UnicodeTranslateError_str(PyObject *self)
{
    Py_ssize_t start;
    Py_ssize_t end;

    if (PyUnicodeTranslateError_GetStart(self, &start))
    return NULL;

    if (PyUnicodeTranslateError_GetEnd(self, &end))
    return NULL;

    if (end==start+1) {
    int badchar = (int)PyUnicode_AS_UNICODE(((PyUnicodeErrorObject *)self)->object)[start];
    char badchar_str[20];
    if (badchar <= 0xff)
        PyOS_snprintf(badchar_str, sizeof(badchar_str), "x%02x", badchar);
    else if (badchar <= 0xffff)
        PyOS_snprintf(badchar_str, sizeof(badchar_str), "u%04x", badchar);
    else
        PyOS_snprintf(badchar_str, sizeof(badchar_str), "U%08x", badchar);
    return PyString_FromFormat(
            "can't translate character u'\\%s' in position %zd: %.400s",
        badchar_str,
        start,
        PyString_AS_STRING(((PyUnicodeErrorObject *)self)->reason)
    );
    }
    return PyString_FromFormat(
        "can't translate characters in position %zd-%zd: %.400s",
        start,
        (end-1),
        PyString_AS_STRING(((PyUnicodeErrorObject *)self)->reason)
    );
}

static PyTypeObject _PyExc_UnicodeTranslateError = {
    PyObject_HEAD_INIT(NULL)
    0,
    EXC_MODULE_NAME "UnicodeTranslateError",
    sizeof(PyUnicodeErrorObject), 0,
    (destructor)UnicodeError_dealloc, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    (reprfunc)UnicodeTranslateError_str, 0, 0, 0,
    Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE | Py_TPFLAGS_HAVE_GC,
    PyDoc_STR("Unicode decoding error."), (traverseproc)UnicodeError_traverse,
    (inquiry)UnicodeError_clear, 0, 0, 0, 0, 0, UnicodeError_members,
    0, &_PyExc_UnicodeError, 0, 0, 0, offsetof(PyUnicodeErrorObject, dict),
    (initproc)UnicodeTranslateError_init, 0, UnicodeTranslateError_new,
};
PyObject *PyExc_UnicodeTranslateError = (PyObject *)&_PyExc_UnicodeTranslateError;

PyObject *
PyUnicodeTranslateError_Create(
    const Py_UNICODE *object, Py_ssize_t length,
    Py_ssize_t start, Py_ssize_t end, const char *reason)
{
    return PyObject_CallFunction(PyExc_UnicodeTranslateError, "u#nns",
    object, length, start, end, reason);
}
#endif


/*
 *    AssertionError extends StandardError
 */
SimpleExtendsException(PyExc_StandardError, AssertionError,
                       "Assertion failed.")


/*
 *    ArithmeticError extends StandardError
 */
SimpleExtendsException(PyExc_StandardError, ArithmeticError,
                       "Base class for arithmetic errors.")


/*
 *    FloatingPointError extends ArithmeticError
 */
SimpleExtendsException(PyExc_ArithmeticError, FloatingPointError,
                       "Floating point operation failed.")


/*
 *    OverflowError extends ArithmeticError
 */
SimpleExtendsException(PyExc_ArithmeticError, OverflowError,
                       "Result too large to be represented.")


/*
 *    ZeroDivisionError extends ArithmeticError
 */
SimpleExtendsException(PyExc_ArithmeticError, ZeroDivisionError,
          "Second argument to a division or modulo operation was zero.")


/*
 *    SystemError extends StandardError
 */
SimpleExtendsException(PyExc_StandardError, SystemError,
    "Internal error in the Python interpreter.\n"
    "\n"
    "Please report this to the Python maintainer, along with the traceback,\n"
    "the Python version, and the hardware/OS platform and version.")


/*
 *    ReferenceError extends StandardError
 */
SimpleExtendsException(PyExc_StandardError, ReferenceError,
                       "Weak ref proxy used after referent went away.")


/*
 *    MemoryError extends StandardError
 */
SimpleExtendsException(PyExc_StandardError, MemoryError, "Out of memory.")


/* Warning category docstrings */

/*
 *    Warning extends Exception
 */
SimpleExtendsException(PyExc_Exception, Warning,
                       "Base class for warning categories.")


/*
 *    UserWarning extends Warning
 */
SimpleExtendsException(PyExc_Warning, UserWarning,
                       "Base class for warnings generated by user code.")


/*
 *    DeprecationWarning extends Warning
 */
SimpleExtendsException(PyExc_Warning, DeprecationWarning,
                       "Base class for warnings about deprecated features.")


/*
 *    PendingDeprecationWarning extends Warning
 */
SimpleExtendsException(PyExc_Warning, PendingDeprecationWarning,
    "Base class for warnings about features which will be deprecated\n"
    "in the future.")


/*
 *    SyntaxWarning extends Warning
 */
SimpleExtendsException(PyExc_Warning, SyntaxWarning,
                       "Base class for warnings about dubious syntax.")


/*
 *    RuntimeWarning extends Warning
 */
SimpleExtendsException(PyExc_Warning, RuntimeWarning,
                 "Base class for warnings about dubious runtime behavior.")


/*
 *    FutureWarning extends Warning
 */
SimpleExtendsException(PyExc_Warning, FutureWarning,
    "Base class for warnings about constructs that will change semantically\n"
    "in the future.")


/*
 *    ImportWarning extends Warning
 */
SimpleExtendsException(PyExc_Warning, ImportWarning,
          "Base class for warnings about probable mistakes in module imports")


/* Pre-computed MemoryError instance.  Best to create this as early as
 * possible and not wait until a MemoryError is actually raised!
 */
PyObject *PyExc_MemoryErrorInst=NULL;

/* module global functions */
static PyMethodDef functions[] = {
    /* Sentinel */
    {NULL, NULL}
};

#define PRE_INIT(TYPE) if (PyType_Ready(&_PyExc_ ## TYPE) < 0) \
    Py_FatalError("exceptions bootstrapping error.");

#define POST_INIT(TYPE) Py_INCREF(PyExc_ ## TYPE); \
    PyModule_AddObject(m, # TYPE, PyExc_ ## TYPE); \
    if (PyDict_SetItemString(bdict, # TYPE, PyExc_ ## TYPE)) \
        Py_FatalError("Module dictionary insertion problem.");

PyMODINIT_FUNC
_PyExc_Init(void) 
{
    PyObject *m, *bltinmod, *bdict;

    PRE_INIT(BaseException)
    PRE_INIT(Exception)
    PRE_INIT(StandardError)
    PRE_INIT(TypeError)
    PRE_INIT(StopIteration)
    PRE_INIT(GeneratorExit)
    PRE_INIT(SystemExit)
    PRE_INIT(KeyboardInterrupt)
    PRE_INIT(ImportError)
    PRE_INIT(EnvironmentError)
    PRE_INIT(IOError)
    PRE_INIT(OSError)
#ifdef MS_WINDOWS
    PRE_INIT(WindowsError)
#endif
#ifdef __VMS
    PRE_INIT(VMSError)
#endif
    PRE_INIT(EOFError)
    PRE_INIT(RuntimeError)
    PRE_INIT(NotImplementedError)
    PRE_INIT(NameError)
    PRE_INIT(UnboundLocalError)
    PRE_INIT(AttributeError)
    PRE_INIT(SyntaxError)
    PRE_INIT(IndentationError)
    PRE_INIT(TabError)
    PRE_INIT(LookupError)
    PRE_INIT(IndexError)
    PRE_INIT(KeyError)
    PRE_INIT(ValueError)
    PRE_INIT(UnicodeError)
#ifdef Py_USING_UNICODE
    PRE_INIT(UnicodeEncodeError)
    PRE_INIT(UnicodeDecodeError)
    PRE_INIT(UnicodeTranslateError)
#endif
    PRE_INIT(AssertionError)
    PRE_INIT(ArithmeticError)
    PRE_INIT(FloatingPointError)
    PRE_INIT(OverflowError)
    PRE_INIT(ZeroDivisionError)
    PRE_INIT(SystemError)
    PRE_INIT(ReferenceError)
    PRE_INIT(MemoryError)
    PRE_INIT(Warning)
    PRE_INIT(UserWarning)
    PRE_INIT(DeprecationWarning)
    PRE_INIT(PendingDeprecationWarning)
    PRE_INIT(SyntaxWarning)
    PRE_INIT(RuntimeWarning)
    PRE_INIT(FutureWarning)
    PRE_INIT(ImportWarning)

    m = Py_InitModule("exceptions", functions);
    if (m == NULL) return;

    bltinmod = PyImport_ImportModule("__builtin__");
    if (bltinmod == NULL)
        Py_FatalError("exceptions bootstrapping error.");
    bdict = PyModule_GetDict(bltinmod);
    if (bdict == NULL)
        Py_FatalError("exceptions bootstrapping error.");

    POST_INIT(BaseException)
    POST_INIT(Exception)
    POST_INIT(StandardError)
    POST_INIT(TypeError)
    POST_INIT(StopIteration)
    POST_INIT(GeneratorExit)
    POST_INIT(SystemExit)
    POST_INIT(KeyboardInterrupt)
    POST_INIT(ImportError)
    POST_INIT(EnvironmentError)
    POST_INIT(IOError)
    POST_INIT(OSError)
#ifdef MS_WINDOWS
    POST_INIT(WindowsError)
#endif
#ifdef __VMS
    POST_INIT(VMSError)
#endif
    POST_INIT(EOFError)
    POST_INIT(RuntimeError)
    POST_INIT(NotImplementedError)
    POST_INIT(NameError)
    POST_INIT(UnboundLocalError)
    POST_INIT(AttributeError)
    POST_INIT(SyntaxError)
    POST_INIT(IndentationError)
    POST_INIT(TabError)
    POST_INIT(LookupError)
    POST_INIT(IndexError)
    POST_INIT(KeyError)
    POST_INIT(ValueError)
    POST_INIT(UnicodeError)
#ifdef Py_USING_UNICODE
    POST_INIT(UnicodeEncodeError)
    POST_INIT(UnicodeDecodeError)
    POST_INIT(UnicodeTranslateError)
#endif
    POST_INIT(AssertionError)
    POST_INIT(ArithmeticError)
    POST_INIT(FloatingPointError)
    POST_INIT(OverflowError)
    POST_INIT(ZeroDivisionError)
    POST_INIT(SystemError)
    POST_INIT(ReferenceError)
    POST_INIT(MemoryError)
    POST_INIT(Warning)
    POST_INIT(UserWarning)
    POST_INIT(DeprecationWarning)
    POST_INIT(PendingDeprecationWarning)
    POST_INIT(SyntaxWarning)
    POST_INIT(RuntimeWarning)
    POST_INIT(FutureWarning)
    POST_INIT(ImportWarning)

    PyExc_MemoryErrorInst = BaseException_new(&_PyExc_MemoryError, NULL, NULL);
    if (!PyExc_MemoryErrorInst)
        Py_FatalError("Cannot pre-allocate MemoryError instance\n");

    Py_DECREF(bltinmod);
}

void
_PyExc_Fini(void)
{
    Py_XDECREF(PyExc_MemoryErrorInst);
    PyExc_MemoryErrorInst = NULL;
}

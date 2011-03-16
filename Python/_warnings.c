#include "Python.h"
#include "frameobject.h"

#define MODULE_NAME "_warnings"

PyDoc_STRVAR(warnings__doc__,
MODULE_NAME " provides basic warning filtering support.\n"
"It is a helper module to speed up interpreter start-up.");

/* Both 'filters' and 'onceregistry' can be set in warnings.py;
   get_warnings_attr() will reset these variables accordingly. */
static PyObject *_filters;  /* List */
static PyObject *_once_registry;  /* Dict */
static PyObject *_default_action; /* String */


static int
check_matched(PyObject *obj, PyObject *arg)
{
    PyObject *result;
    int rc;

    if (obj == Py_None)
        return 1;
    result = PyObject_CallMethod(obj, "match", "O", arg);
    if (result == NULL)
        return -1;

    rc = PyObject_IsTrue(result);
    Py_DECREF(result);
    return rc;
}

/*
   Returns a new reference.
   A NULL return value can mean false or an error.
*/
static PyObject *
get_warnings_attr(const char *attr)
{
    static PyObject *warnings_str = NULL;
    PyObject *all_modules;
    PyObject *warnings_module;
    int result;

    if (warnings_str == NULL) {
        warnings_str = PyUnicode_InternFromString("warnings");
        if (warnings_str == NULL)
            return NULL;
    }

    all_modules = PyImport_GetModuleDict();
    result = PyDict_Contains(all_modules, warnings_str);
    if (result == -1 || result == 0)
        return NULL;

    warnings_module = PyDict_GetItem(all_modules, warnings_str);
    if (!PyObject_HasAttrString(warnings_module, attr))
            return NULL;
    return PyObject_GetAttrString(warnings_module, attr);
}


static PyObject *
get_once_registry(void)
{
    PyObject *registry;

    registry = get_warnings_attr("onceregistry");
    if (registry == NULL) {
        if (PyErr_Occurred())
            return NULL;
        return _once_registry;
    }
    Py_DECREF(_once_registry);
    _once_registry = registry;
    return registry;
}


static PyObject *
get_default_action(void)
{
    PyObject *default_action;

    default_action = get_warnings_attr("defaultaction");
    if (default_action == NULL) {
        if (PyErr_Occurred()) {
            return NULL;
        }
        return _default_action;
    }

    Py_DECREF(_default_action);
    _default_action = default_action;
    return default_action;
}


/* The item is a borrowed reference. */
static const char *
get_filter(PyObject *category, PyObject *text, Py_ssize_t lineno,
           PyObject *module, PyObject **item)
{
    PyObject *action;
    Py_ssize_t i;
    PyObject *warnings_filters;

    warnings_filters = get_warnings_attr("filters");
    if (warnings_filters == NULL) {
        if (PyErr_Occurred())
            return NULL;
    }
    else {
        Py_DECREF(_filters);
        _filters = warnings_filters;
    }

    if (_filters == NULL || !PyList_Check(_filters)) {
        PyErr_SetString(PyExc_ValueError,
                        MODULE_NAME ".filters must be a list");
        return NULL;
    }

    /* _filters could change while we are iterating over it. */
    for (i = 0; i < PyList_GET_SIZE(_filters); i++) {
        PyObject *tmp_item, *action, *msg, *cat, *mod, *ln_obj;
        Py_ssize_t ln;
        int is_subclass, good_msg, good_mod;

        tmp_item = *item = PyList_GET_ITEM(_filters, i);
        if (PyTuple_Size(tmp_item) != 5) {
            PyErr_Format(PyExc_ValueError,
                         MODULE_NAME ".filters item %zd isn't a 5-tuple", i);
            return NULL;
        }

        /* Python code: action, msg, cat, mod, ln = item */
        action = PyTuple_GET_ITEM(tmp_item, 0);
        msg = PyTuple_GET_ITEM(tmp_item, 1);
        cat = PyTuple_GET_ITEM(tmp_item, 2);
        mod = PyTuple_GET_ITEM(tmp_item, 3);
        ln_obj = PyTuple_GET_ITEM(tmp_item, 4);

        good_msg = check_matched(msg, text);
        good_mod = check_matched(mod, module);
        is_subclass = PyObject_IsSubclass(category, cat);
        ln = PyLong_AsSsize_t(ln_obj);
        if (good_msg == -1 || good_mod == -1 || is_subclass == -1 ||
            (ln == -1 && PyErr_Occurred()))
            return NULL;

        if (good_msg && is_subclass && good_mod && (ln == 0 || lineno == ln))
            return _PyUnicode_AsString(action);
    }

    action = get_default_action();
    if (action != NULL) {
        return _PyUnicode_AsString(action);
    }

    PyErr_SetString(PyExc_ValueError,
                    MODULE_NAME ".defaultaction not found");
    return NULL;
}


static int
already_warned(PyObject *registry, PyObject *key, int should_set)
{
    PyObject *already_warned;

    if (key == NULL)
        return -1;

    already_warned = PyDict_GetItem(registry, key);
    if (already_warned != NULL) {
        int rc = PyObject_IsTrue(already_warned);
        if (rc != 0)
            return rc;
    }

    /* This warning wasn't found in the registry, set it. */
    if (should_set)
        return PyDict_SetItem(registry, key, Py_True);
    return 0;
}

/* New reference. */
static PyObject *
normalize_module(PyObject *filename)
{
    PyObject *module;
    const char *mod_str;
    Py_ssize_t len;

    int rc = PyObject_IsTrue(filename);
    if (rc == -1)
        return NULL;
    else if (rc == 0)
        return PyUnicode_FromString("<unknown>");

    mod_str = _PyUnicode_AsString(filename);
    if (mod_str == NULL)
            return NULL;
    len = PyUnicode_GetSize(filename);
    if (len < 0)
        return NULL;
    if (len >= 3 &&
        strncmp(mod_str + (len - 3), ".py", 3) == 0) {
        module = PyUnicode_FromStringAndSize(mod_str, len-3);
    }
    else {
        module = filename;
        Py_INCREF(module);
    }
    return module;
}

static int
update_registry(PyObject *registry, PyObject *text, PyObject *category,
                int add_zero)
{
    PyObject *altkey, *zero = NULL;
    int rc;

    if (add_zero) {
        zero = PyLong_FromLong(0);
        if (zero == NULL)
            return -1;
        altkey = PyTuple_Pack(3, text, category, zero);
    }
    else
        altkey = PyTuple_Pack(2, text, category);

    rc = already_warned(registry, altkey, 1);
    Py_XDECREF(zero);
    Py_XDECREF(altkey);
    return rc;
}

static void
show_warning(PyObject *filename, int lineno, PyObject *text, PyObject
                *category, PyObject *sourceline)
{
    PyObject *f_stderr;
    PyObject *name;
    char lineno_str[128];

    PyOS_snprintf(lineno_str, sizeof(lineno_str), ":%d: ", lineno);

    name = PyObject_GetAttrString(category, "__name__");
    if (name == NULL)  /* XXX Can an object lack a '__name__' attribute? */
        return;

    f_stderr = PySys_GetObject("stderr");
    if (f_stderr == NULL) {
        fprintf(stderr, "lost sys.stderr\n");
        Py_DECREF(name);
        return;
    }

    /* Print "filename:lineno: category: text\n" */
    PyFile_WriteObject(filename, f_stderr, Py_PRINT_RAW);
    PyFile_WriteString(lineno_str, f_stderr);
    PyFile_WriteObject(name, f_stderr, Py_PRINT_RAW);
    PyFile_WriteString(": ", f_stderr);
    PyFile_WriteObject(text, f_stderr, Py_PRINT_RAW);
    PyFile_WriteString("\n", f_stderr);
    Py_XDECREF(name);

    /* Print "  source_line\n" */
    if (sourceline) {
        char *source_line_str = _PyUnicode_AsString(sourceline);
        if (source_line_str == NULL)
                return;
        while (*source_line_str == ' ' || *source_line_str == '\t' ||
                *source_line_str == '\014')
            source_line_str++;

        PyFile_WriteString(source_line_str, f_stderr);
        PyFile_WriteString("\n", f_stderr);
    }
    else
        if (_Py_DisplaySourceLine(f_stderr, filename, lineno, 2) < 0)
                return;
    PyErr_Clear();
}

static PyObject *
warn_explicit(PyObject *category, PyObject *message,
              PyObject *filename, int lineno,
              PyObject *module, PyObject *registry, PyObject *sourceline)
{
    PyObject *key = NULL, *text = NULL, *result = NULL, *lineno_obj = NULL;
    PyObject *item = Py_None;
    const char *action;
    int rc;

    if (registry && !PyDict_Check(registry) && (registry != Py_None)) {
        PyErr_SetString(PyExc_TypeError, "'registry' must be a dict");
        return NULL;
    }

    /* Normalize module. */
    if (module == NULL) {
        module = normalize_module(filename);
        if (module == NULL)
            return NULL;
    }
    else
        Py_INCREF(module);

    /* Normalize message. */
    Py_INCREF(message);  /* DECREF'ed in cleanup. */
    rc = PyObject_IsInstance(message, PyExc_Warning);
    if (rc == -1) {
        goto cleanup;
    }
    if (rc == 1) {
        text = PyObject_Str(message);
        if (text == NULL)
            goto cleanup;
        category = (PyObject*)message->ob_type;
    }
    else {
        text = message;
        message = PyObject_CallFunction(category, "O", message);
        if (message == NULL)
            goto cleanup;
    }

    lineno_obj = PyLong_FromLong(lineno);
    if (lineno_obj == NULL)
        goto cleanup;

    /* Create key. */
    key = PyTuple_Pack(3, text, category, lineno_obj);
    if (key == NULL)
        goto cleanup;

    if ((registry != NULL) && (registry != Py_None)) {
        rc = already_warned(registry, key, 0);
        if (rc == -1)
            goto cleanup;
        else if (rc == 1)
            goto return_none;
        /* Else this warning hasn't been generated before. */
    }

    action = get_filter(category, text, lineno, module, &item);
    if (action == NULL)
        goto cleanup;

    if (strcmp(action, "error") == 0) {
        PyErr_SetObject(category, message);
        goto cleanup;
    }

    /* Store in the registry that we've been here, *except* when the action
       is "always". */
    rc = 0;
    if (strcmp(action, "always") != 0) {
        if (registry != NULL && registry != Py_None &&
                PyDict_SetItem(registry, key, Py_True) < 0)
            goto cleanup;
        else if (strcmp(action, "ignore") == 0)
            goto return_none;
        else if (strcmp(action, "once") == 0) {
            if (registry == NULL || registry == Py_None) {
                registry = get_once_registry();
                if (registry == NULL)
                    goto cleanup;
            }
            /* _once_registry[(text, category)] = 1 */
            rc = update_registry(registry, text, category, 0);
        }
        else if (strcmp(action, "module") == 0) {
            /* registry[(text, category, 0)] = 1 */
            if (registry != NULL && registry != Py_None)
                rc = update_registry(registry, text, category, 0);
        }
        else if (strcmp(action, "default") != 0) {
            PyObject *to_str = PyObject_Str(item);
            const char *err_str = "???";

            if (to_str != NULL) {
                err_str = _PyUnicode_AsString(to_str);
                if (err_str == NULL)
                        goto cleanup;
            }
            PyErr_Format(PyExc_RuntimeError,
                        "Unrecognized action (%s) in warnings.filters:\n %s",
                        action, err_str);
            Py_XDECREF(to_str);
            goto cleanup;
        }
    }

    if (rc == 1)  /* Already warned for this module. */
        goto return_none;
    if (rc == 0) {
        PyObject *show_fxn = get_warnings_attr("showwarning");
        if (show_fxn == NULL) {
            if (PyErr_Occurred())
                goto cleanup;
            show_warning(filename, lineno, text, category, sourceline);
        }
        else {
            PyObject *res;

            if (!PyMethod_Check(show_fxn) && !PyFunction_Check(show_fxn)) {
                PyErr_SetString(PyExc_TypeError,
                                "warnings.showwarning() must be set to a "
                                "function or method");
                Py_DECREF(show_fxn);
                goto cleanup;
            }

            res = PyObject_CallFunctionObjArgs(show_fxn, message, category,
                                                filename, lineno_obj,
                                                NULL);
            Py_DECREF(show_fxn);
            Py_XDECREF(res);
            if (res == NULL)
                goto cleanup;
        }
    }
    else /* if (rc == -1) */
        goto cleanup;

 return_none:
    result = Py_None;
    Py_INCREF(result);

 cleanup:
    Py_XDECREF(key);
    Py_XDECREF(text);
    Py_XDECREF(lineno_obj);
    Py_DECREF(module);
    Py_XDECREF(message);
    return result;  /* Py_None or NULL. */
}

/* filename, module, and registry are new refs, globals is borrowed */
/* Returns 0 on error (no new refs), 1 on success */
static int
setup_context(Py_ssize_t stack_level, PyObject **filename, int *lineno,
              PyObject **module, PyObject **registry)
{
    PyObject *globals;

    /* Setup globals and lineno. */
    PyFrameObject *f = PyThreadState_GET()->frame;
    while (--stack_level > 0 && f != NULL)
        f = f->f_back;

    if (f == NULL) {
        globals = PyThreadState_Get()->interp->sysdict;
        *lineno = 1;
    }
    else {
        globals = f->f_globals;
        *lineno = PyFrame_GetLineNumber(f);
    }

    *module = NULL;

    /* Setup registry. */
    assert(globals != NULL);
    assert(PyDict_Check(globals));
    *registry = PyDict_GetItemString(globals, "__warningregistry__");
    if (*registry == NULL) {
        int rc;

        *registry = PyDict_New();
        if (*registry == NULL)
            return 0;

         rc = PyDict_SetItemString(globals, "__warningregistry__", *registry);
         if (rc < 0)
            goto handle_error;
    }
    else
        Py_INCREF(*registry);

    /* Setup module. */
    *module = PyDict_GetItemString(globals, "__name__");
    if (*module == NULL) {
        *module = PyUnicode_FromString("<string>");
        if (*module == NULL)
            goto handle_error;
    }
    else
        Py_INCREF(*module);

    /* Setup filename. */
    *filename = PyDict_GetItemString(globals, "__file__");
    if (*filename != NULL) {
        Py_ssize_t len = PyUnicode_GetSize(*filename);
        Py_UNICODE *unicode = PyUnicode_AS_UNICODE(*filename);

        /* if filename.lower().endswith((".pyc", ".pyo")): */
        if (len >= 4 &&
            unicode[len-4] == '.' &&
            Py_UNICODE_TOLOWER(unicode[len-3]) == 'p' &&
            Py_UNICODE_TOLOWER(unicode[len-2]) == 'y' &&
            (Py_UNICODE_TOLOWER(unicode[len-1]) == 'c' ||
                Py_UNICODE_TOLOWER(unicode[len-1]) == 'o'))
        {
            *filename = PyUnicode_FromUnicode(unicode, len-1);
            if (*filename == NULL)
                goto handle_error;
        }
        else
            Py_INCREF(*filename);
    }
    else {
        const char *module_str = _PyUnicode_AsString(*module);
        if (module_str == NULL)
                goto handle_error;
        if (strcmp(module_str, "__main__") == 0) {
            PyObject *argv = PySys_GetObject("argv");
            if (argv != NULL && PyList_Size(argv) > 0) {
                int is_true;
                *filename = PyList_GetItem(argv, 0);
                Py_INCREF(*filename);
                /* If sys.argv[0] is false, then use '__main__'. */
                is_true = PyObject_IsTrue(*filename);
                if (is_true < 0) {
                    Py_DECREF(*filename);
                    goto handle_error;
                }
                else if (!is_true) {
                    Py_DECREF(*filename);
                    *filename = PyUnicode_FromString("__main__");
                    if (*filename == NULL)
                        goto handle_error;
                }
            }
            else {
                /* embedded interpreters don't have sys.argv, see bug #839151 */
                *filename = PyUnicode_FromString("__main__");
                    if (*filename == NULL)
                        goto handle_error;
            }
        }
        if (*filename == NULL) {
            *filename = *module;
            Py_INCREF(*filename);
        }
    }

    return 1;

 handle_error:
    /* filename not XDECREF'ed here as there is no way to jump here with a
       dangling reference. */
    Py_XDECREF(*registry);
    Py_XDECREF(*module);
    return 0;
}

static PyObject *
get_category(PyObject *message, PyObject *category)
{
    int rc;

    /* Get category. */
    rc = PyObject_IsInstance(message, PyExc_Warning);
    if (rc == -1)
        return NULL;

    if (rc == 1)
        category = (PyObject*)message->ob_type;
    else if (category == NULL)
        category = PyExc_UserWarning;

    /* Validate category. */
    rc = PyObject_IsSubclass(category, PyExc_Warning);
    if (rc == -1)
        return NULL;
    if (rc == 0) {
        PyErr_SetString(PyExc_ValueError,
                        "category is not a subclass of Warning");
        return NULL;
    }

    return category;
}

static PyObject *
do_warn(PyObject *message, PyObject *category, Py_ssize_t stack_level)
{
    PyObject *filename, *module, *registry, *res;
    int lineno;

    if (!setup_context(stack_level, &filename, &lineno, &module, &registry))
        return NULL;

    res = warn_explicit(category, message, filename, lineno, module, registry,
                        NULL);
    Py_DECREF(filename);
    Py_DECREF(registry);
    Py_DECREF(module);
    return res;
}

static PyObject *
warnings_warn(PyObject *self, PyObject *args, PyObject *kwds)
{
    static char *kw_list[] = { "message", "category", "stacklevel", 0 };
    PyObject *message, *category = NULL;
    Py_ssize_t stack_level = 1;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "O|On:warn", kw_list,
                                     &message, &category, &stack_level))
        return NULL;

    category = get_category(message, category);
    if (category == NULL)
        return NULL;
    return do_warn(message, category, stack_level);
}

static PyObject *
warnings_warn_explicit(PyObject *self, PyObject *args, PyObject *kwds)
{
    static char *kwd_list[] = {"message", "category", "filename", "lineno",
                                "module", "registry", "module_globals", 0};
    PyObject *message;
    PyObject *category;
    PyObject *filename;
    int lineno;
    PyObject *module = NULL;
    PyObject *registry = NULL;
    PyObject *module_globals = NULL;

    if (!PyArg_ParseTupleAndKeywords(args, kwds, "OOOi|OOO:warn_explicit",
                kwd_list, &message, &category, &filename, &lineno, &module,
                &registry, &module_globals))
        return NULL;

    if (module_globals) {
        static PyObject *get_source_name = NULL;
        static PyObject *splitlines_name = NULL;
        PyObject *loader;
        PyObject *module_name;
        PyObject *source;
        PyObject *source_list;
        PyObject *source_line;
        PyObject *returned;

        if (get_source_name == NULL) {
            get_source_name = PyUnicode_InternFromString("get_source");
            if (!get_source_name)
                return NULL;
        }
        if (splitlines_name == NULL) {
            splitlines_name = PyUnicode_InternFromString("splitlines");
            if (!splitlines_name)
                return NULL;
        }

        /* Check/get the requisite pieces needed for the loader. */
        loader = PyDict_GetItemString(module_globals, "__loader__");
        module_name = PyDict_GetItemString(module_globals, "__name__");

        if (loader == NULL || module_name == NULL)
            goto standard_call;

        /* Make sure the loader implements the optional get_source() method. */
        if (!PyObject_HasAttrString(loader, "get_source"))
                goto standard_call;
        /* Call get_source() to get the source code. */
        source = PyObject_CallMethodObjArgs(loader, get_source_name,
                                                module_name, NULL);
        if (!source)
            return NULL;
        else if (source == Py_None) {
            Py_DECREF(Py_None);
            goto standard_call;
        }

        /* Split the source into lines. */
        source_list = PyObject_CallMethodObjArgs(source, splitlines_name,
                                                    NULL);
        Py_DECREF(source);
        if (!source_list)
            return NULL;

        /* Get the source line. */
        source_line = PyList_GetItem(source_list, lineno-1);
        if (!source_line) {
            Py_DECREF(source_list);
            return NULL;
        }

        /* Handle the warning. */
        returned = warn_explicit(category, message, filename, lineno, module,
                            registry, source_line);
        Py_DECREF(source_list);
        return returned;
    }

 standard_call:
    return warn_explicit(category, message, filename, lineno, module,
                                registry, NULL);
}


/* Function to issue a warning message; may raise an exception. */

static int
warn_unicode(PyObject *category, PyObject *message,
             Py_ssize_t stack_level)
{
    PyObject *res;

    if (category == NULL)
        category = PyExc_RuntimeWarning;

    res = do_warn(message, category, stack_level);
    if (res == NULL)
        return -1;
    Py_DECREF(res);

    return 0;
}

int
PyErr_WarnFormat(PyObject *category, Py_ssize_t stack_level,
                 const char *format, ...)
{
    int ret;
    PyObject *message;
    va_list vargs;

#ifdef HAVE_STDARG_PROTOTYPES
    va_start(vargs, format);
#else
    va_start(vargs);
#endif
    message = PyUnicode_FromFormatV(format, vargs);
    if (message != NULL) {
        ret = warn_unicode(category, message, stack_level);
        Py_DECREF(message);
    }
    else
        ret = -1;
    va_end(vargs);
    return ret;
}

int
PyErr_WarnEx(PyObject *category, const char *text, Py_ssize_t stack_level)
{
    int ret;
    PyObject *message = PyUnicode_FromString(text);
    if (message == NULL)
        return -1;
    ret = warn_unicode(category, message, stack_level);
    Py_DECREF(message);
    return ret;
}

/* PyErr_Warn is only for backwards compatibility and will be removed.
   Use PyErr_WarnEx instead. */

#undef PyErr_Warn

PyAPI_FUNC(int)
PyErr_Warn(PyObject *category, char *text)
{
    return PyErr_WarnEx(category, text, 1);
}

/* Warning with explicit origin */
int
PyErr_WarnExplicit(PyObject *category, const char *text,
                   const char *filename_str, int lineno,
                   const char *module_str, PyObject *registry)
{
    PyObject *res;
    PyObject *message = PyUnicode_FromString(text);
    PyObject *filename = PyUnicode_DecodeFSDefault(filename_str);
    PyObject *module = NULL;
    int ret = -1;

    if (message == NULL || filename == NULL)
        goto exit;
    if (module_str != NULL) {
        module = PyUnicode_FromString(module_str);
            if (module == NULL)
                goto exit;
    }

    if (category == NULL)
        category = PyExc_RuntimeWarning;
    res = warn_explicit(category, message, filename, lineno, module, registry,
                        NULL);
    if (res == NULL)
        goto exit;
    Py_DECREF(res);
    ret = 0;

 exit:
    Py_XDECREF(message);
    Py_XDECREF(module);
    Py_XDECREF(filename);
    return ret;
}


PyDoc_STRVAR(warn_doc,
"Issue a warning, or maybe ignore it or raise an exception.");

PyDoc_STRVAR(warn_explicit_doc,
"Low-level inferface to warnings functionality.");

static PyMethodDef warnings_functions[] = {
    {"warn", (PyCFunction)warnings_warn, METH_VARARGS | METH_KEYWORDS,
        warn_doc},
    {"warn_explicit", (PyCFunction)warnings_warn_explicit,
        METH_VARARGS | METH_KEYWORDS, warn_explicit_doc},
    /* XXX(brett.cannon): add showwarning? */
    /* XXX(brett.cannon): Reasonable to add formatwarning? */
    {NULL, NULL}                /* sentinel */
};


static PyObject *
create_filter(PyObject *category, const char *action)
{
    static PyObject *ignore_str = NULL;
    static PyObject *error_str = NULL;
    static PyObject *default_str = NULL;
    static PyObject *always_str = NULL;
    PyObject *action_obj = NULL;
    PyObject *lineno, *result;

    if (!strcmp(action, "ignore")) {
        if (ignore_str == NULL) {
            ignore_str = PyUnicode_InternFromString("ignore");
            if (ignore_str == NULL)
                return NULL;
        }
        action_obj = ignore_str;
    }
    else if (!strcmp(action, "error")) {
        if (error_str == NULL) {
            error_str = PyUnicode_InternFromString("error");
            if (error_str == NULL)
                return NULL;
        }
        action_obj = error_str;
    }
    else if (!strcmp(action, "default")) {
        if (default_str == NULL) {
            default_str = PyUnicode_InternFromString("default");
            if (default_str == NULL)
                return NULL;
        }
        action_obj = default_str;
    }
    else if (!strcmp(action, "always")) {
        if (always_str == NULL) {
            always_str = PyUnicode_InternFromString("always");
            if (always_str == NULL)
                return NULL;
        }
        action_obj = always_str;
    }
    else {
        Py_FatalError("unknown action");
    }

    /* This assumes the line number is zero for now. */
    lineno = PyLong_FromLong(0);
    if (lineno == NULL)
        return NULL;
    result = PyTuple_Pack(5, action_obj, Py_None, category, Py_None, lineno);
    Py_DECREF(lineno);
    return result;
}

static PyObject *
init_filters(void)
{
    /* Don't silence DeprecationWarning if -3 was used. */
    PyObject *filters = PyList_New(5);
    unsigned int pos = 0;  /* Post-incremented in each use. */
    unsigned int x;
    const char *bytes_action, *resource_action;

    if (filters == NULL)
        return NULL;

    PyList_SET_ITEM(filters, pos++,
                    create_filter(PyExc_DeprecationWarning, "ignore"));
    PyList_SET_ITEM(filters, pos++,
                    create_filter(PyExc_PendingDeprecationWarning, "ignore"));
    PyList_SET_ITEM(filters, pos++,
                    create_filter(PyExc_ImportWarning, "ignore"));
    if (Py_BytesWarningFlag > 1)
        bytes_action = "error";
    else if (Py_BytesWarningFlag)
        bytes_action = "default";
    else
        bytes_action = "ignore";
    PyList_SET_ITEM(filters, pos++, create_filter(PyExc_BytesWarning,
                    bytes_action));
    /* resource usage warnings are enabled by default in pydebug mode */
#ifdef Py_DEBUG
    resource_action = "always";
#else
    resource_action = "ignore";
#endif
    PyList_SET_ITEM(filters, pos++, create_filter(PyExc_ResourceWarning,
                    resource_action));
    for (x = 0; x < pos; x += 1) {
        if (PyList_GET_ITEM(filters, x) == NULL) {
            Py_DECREF(filters);
            return NULL;
        }
    }

    return filters;
}

static struct PyModuleDef warningsmodule = {
        PyModuleDef_HEAD_INIT,
        MODULE_NAME,
        warnings__doc__,
        0,
        warnings_functions,
        NULL,
        NULL,
        NULL,
        NULL
};


PyMODINIT_FUNC
_PyWarnings_Init(void)
{
    PyObject *m;

    m = PyModule_Create(&warningsmodule);
    if (m == NULL)
        return NULL;

    _filters = init_filters();
    if (_filters == NULL)
        return NULL;
    Py_INCREF(_filters);
    if (PyModule_AddObject(m, "filters", _filters) < 0)
        return NULL;

    _once_registry = PyDict_New();
    if (_once_registry == NULL)
        return NULL;
    Py_INCREF(_once_registry);
    if (PyModule_AddObject(m, "_onceregistry", _once_registry) < 0)
        return NULL;

    _default_action = PyUnicode_FromString("default");
    if (_default_action == NULL)
        return NULL;
    if (PyModule_AddObject(m, "_defaultaction", _default_action) < 0)
        return NULL;
    return m;
}

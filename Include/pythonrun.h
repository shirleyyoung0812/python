
/* Interfaces to parse and execute pieces of python code */

#ifndef Py_PYTHONRUN_H
#define Py_PYTHONRUN_H
#ifdef __cplusplus
extern "C" {
#endif

#define PyCF_MASK (CO_FUTURE_DIVISION)
#define PyCF_MASK_OBSOLETE (CO_GENERATOR_ALLOWED | CO_NESTED)

typedef struct {
	int cf_flags;  /* bitmask of CO_xxx flags relevant to future */
} PyCompilerFlags;

PyAPI_FUNC(void) Py_SetProgramName(char *);
PyAPI_FUNC(char *) Py_GetProgramName(void);

PyAPI_FUNC(void) Py_SetPythonHome(char *);
PyAPI_FUNC(char *) Py_GetPythonHome(void);

PyAPI_FUNC(void) Py_Initialize(void);
PyAPI_FUNC(void) Py_Finalize(void);
PyAPI_FUNC(int) Py_IsInitialized(void);
PyAPI_FUNC(PyThreadState *) Py_NewInterpreter(void);
PyAPI_FUNC(void) Py_EndInterpreter(PyThreadState *);

PyAPI_FUNC(int) PyRun_AnyFile(FILE *, char *);
PyAPI_FUNC(int) PyRun_AnyFileEx(FILE *, char *, int);

PyAPI_FUNC(int) PyRun_AnyFileFlags(FILE *, char *, PyCompilerFlags *);
PyAPI_FUNC(int) PyRun_AnyFileExFlags(FILE *, char *, int, PyCompilerFlags *);

PyAPI_FUNC(int) PyRun_SimpleString(char *);
PyAPI_FUNC(int) PyRun_SimpleStringFlags(char *, PyCompilerFlags *);
PyAPI_FUNC(int) PyRun_SimpleFile(FILE *, char *);
PyAPI_FUNC(int) PyRun_SimpleFileEx(FILE *, char *, int);
PyAPI_FUNC(int) PyRun_SimpleFileExFlags(FILE *, char *, int, PyCompilerFlags *);
PyAPI_FUNC(int) PyRun_InteractiveOne(FILE *, char *);
PyAPI_FUNC(int) PyRun_InteractiveOneFlags(FILE *, char *, PyCompilerFlags *);
PyAPI_FUNC(int) PyRun_InteractiveLoop(FILE *, char *);
PyAPI_FUNC(int) PyRun_InteractiveLoopFlags(FILE *, char *, PyCompilerFlags *);

PyAPI_FUNC(struct _node *) PyParser_SimpleParseString(char *, int);
PyAPI_FUNC(struct _node *) PyParser_SimpleParseFile(FILE *, char *, int);
PyAPI_FUNC(struct _node *) PyParser_SimpleParseStringFlags(char *, int, int);
PyAPI_FUNC(struct _node *) PyParser_SimpleParseStringFlagsFilename(char *,
								  char *,
								  int,
								  int);
PyAPI_FUNC(struct _node *) PyParser_SimpleParseFileFlags(FILE *, char *,
							int, int);

PyAPI_FUNC(PyObject *) PyRun_String(char *, int, PyObject *, PyObject *);
PyAPI_FUNC(PyObject *) PyRun_File(FILE *, char *, int, PyObject *, PyObject *);
PyAPI_FUNC(PyObject *) PyRun_FileEx(FILE *, char *, int,
				   PyObject *, PyObject *, int);
PyAPI_FUNC(PyObject *) PyRun_StringFlags(char *, int, PyObject *, PyObject *,
					PyCompilerFlags *);
PyAPI_FUNC(PyObject *) PyRun_FileFlags(FILE *, char *, int, PyObject *, 
				      PyObject *, PyCompilerFlags *);
PyAPI_FUNC(PyObject *) PyRun_FileExFlags(FILE *, char *, int, PyObject *, 
					PyObject *, int, PyCompilerFlags *);

PyAPI_FUNC(PyObject *) Py_CompileString(char *, char *, int);
PyAPI_FUNC(PyObject *) Py_CompileStringFlags(char *, char *, int,
					    PyCompilerFlags *);
PyAPI_FUNC(struct symtable *) Py_SymtableString(char *, char *, int);

PyAPI_FUNC(void) PyErr_Print(void);
PyAPI_FUNC(void) PyErr_PrintEx(int);
PyAPI_FUNC(void) PyErr_Display(PyObject *, PyObject *, PyObject *);

PyAPI_FUNC(int) Py_AtExit(void (*func)(void));

PyAPI_FUNC(void) Py_Exit(int);

PyAPI_FUNC(int) Py_FdIsInteractive(FILE *, char *);

/* Bootstrap */
PyAPI_FUNC(int) Py_Main(int argc, char **argv);

/* In getpath.c */
PyAPI_FUNC(char *) Py_GetProgramFullPath(void);
PyAPI_FUNC(char *) Py_GetPrefix(void);
PyAPI_FUNC(char *) Py_GetExecPrefix(void);
PyAPI_FUNC(char *) Py_GetPath(void);

/* In their own files */
PyAPI_FUNC(const char *) Py_GetVersion(void);
PyAPI_FUNC(const char *) Py_GetPlatform(void);
PyAPI_FUNC(const char *) Py_GetCopyright(void);
PyAPI_FUNC(const char *) Py_GetCompiler(void);
PyAPI_FUNC(const char *) Py_GetBuildInfo(void);

/* Internal -- various one-time initializations */
PyAPI_FUNC(PyObject *) _PyBuiltin_Init(void);
PyAPI_FUNC(PyObject *) _PySys_Init(void);
PyAPI_FUNC(void) _PyImport_Init(void);
PyAPI_FUNC(void) _PyExc_Init(void);

/* Various internal finalizers */
PyAPI_FUNC(void) _PyExc_Fini(void);
PyAPI_FUNC(void) _PyImport_Fini(void);
PyAPI_FUNC(void) PyMethod_Fini(void);
PyAPI_FUNC(void) PyFrame_Fini(void);
PyAPI_FUNC(void) PyCFunction_Fini(void);
PyAPI_FUNC(void) PyTuple_Fini(void);
PyAPI_FUNC(void) PyString_Fini(void);
PyAPI_FUNC(void) PyInt_Fini(void);
PyAPI_FUNC(void) PyFloat_Fini(void);
PyAPI_FUNC(void) PyOS_FiniInterrupts(void);

/* Stuff with no proper home (yet) */
PyAPI_FUNC(char *) PyOS_Readline(char *);
PyAPI_FUNC(int) (*PyOS_InputHook)(void);
PyAPI_FUNC(char) *(*PyOS_ReadlineFunctionPointer)(char *);

/* Stack size, in "pointers" (so we get extra safety margins
   on 64-bit platforms).  On a 32-bit platform, this translates
   to a 8k margin. */
#define PYOS_STACK_MARGIN 2048

#if defined(WIN32) && !defined(MS_WIN64) && defined(_MSC_VER)
/* Enable stack checking under Microsoft C */
#define USE_STACKCHECK
#endif

#ifdef USE_STACKCHECK
/* Check that we aren't overflowing our stack */
PyAPI_FUNC(int) PyOS_CheckStack(void);
#endif

/* Signals */
typedef void (*PyOS_sighandler_t)(int);
PyAPI_FUNC(PyOS_sighandler_t) PyOS_getsig(int);
PyAPI_FUNC(PyOS_sighandler_t) PyOS_setsig(int, PyOS_sighandler_t);


#ifdef __cplusplus
}
#endif
#endif /* !Py_PYTHONRUN_H */

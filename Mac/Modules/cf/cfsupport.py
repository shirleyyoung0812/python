# This script generates a Python interface for an Apple Macintosh Manager.
# It uses the "bgen" package to generate C code.
# The function specifications are generated by scanning the mamager's header file,
# using the "scantools" package (customized for this particular manager).

#error missing SetActionFilter

import string

# Declarations that change for each manager
MODNAME = 'CF'				# The name of the module

# The following is *usually* unchanged but may still require tuning
MODPREFIX = MODNAME			# The prefix for module-wide routines
INPUTFILE = string.lower(MODPREFIX) + 'gen.py' # The file generated by the scanner
OUTPUTFILE = MODNAME + "module.c"	# The file generated by this program

from macsupport import *

# Create the type objects

includestuff = includestuff + """
#ifdef WITHOUT_FRAMEWORKS
#include <CoreFoundation.h>
#else
#include <CoreFoundation.h>
#endif

/* For now we declare them forward here. They'll go to mactoolbox later */
extern PyObject *CFTypeRefObj_New(CFTypeRef);
extern int CFTypeRefObj_Convert(PyObject *, CFTypeRef *);
extern PyObject *CFStringRefObj_New(CFStringRef);
extern int CFStringRefObj_Convert(PyObject *, CFStringRef *);

#ifdef NOTYET_USE_TOOLBOX_OBJECT_GLUE
//extern PyObject *_CFTypeRefObj_New(CFTypeRef);
//extern int _CFTypeRefObj_Convert(PyObject *, CFTypeRef *);

//#define CFTypeRefObj_New _CFTypeRefObj_New
//#define CFTypeRefObj_Convert _CFTypeRefObj_Convert
#endif

"""

initstuff = initstuff + """
//	PyMac_INIT_TOOLBOX_OBJECT_NEW(Track, TrackObj_New);
//	PyMac_INIT_TOOLBOX_OBJECT_CONVERT(Track, TrackObj_Convert);
"""

Boolean = Type("Boolean", "l")
CFTypeID = Type("CFTypeID", "l") # XXXX a guess, seems better than OSTypeType.
CFHashCode = Type("CFHashCode", "l")
CFIndex = Type("CFIndex", "l")
CFOptionFlags = Type("CFOptionFlags", "l")
## CFStringRef = XXXX
CFAllocatorRef = FakeType("(CFAllocatorRef)NULL")

# The real objects
CFTypeRef = OpaqueByValueType("CFTypeRef", "CFTypeRefObj")
CFStringRef = OpaqueByValueType("CFStringRef", "CFStringRefObj")

# Our (opaque) objects

class MyGlobalObjectDefinition(GlobalObjectDefinition):
	def outputCheckNewArg(self):
		Output("if (itself == NULL) return PyMac_Error(resNotFound);")
		Output("CFRetain(itself);")
	def outputStructMembers(self):
		GlobalObjectDefinition.outputStructMembers(self)
		Output("void (*ob_freeit)(CFTypeRef ptr);")
	def outputInitStructMembers(self):
		GlobalObjectDefinition.outputInitStructMembers(self)
##		Output("it->ob_freeit = NULL;")
		Output("it->ob_freeit = CFRelease;")
	def outputCheckConvertArg(self):
		Out("""
		if (v == Py_None) { *p_itself = NULL; return 1; }
		/* Check for other CF objects here */
		""")
	def outputCleanupStructMembers(self):
		Output("if (self->ob_freeit && self->ob_itself)")
		OutLbrace()
		Output("self->ob_freeit((CFTypeRef)self->ob_itself);")
		OutRbrace()
		
	def outputCompare(self):
		Output()
		Output("static int %s_compare(%s *self, %s *other)", self.prefix, self.objecttype, self.objecttype)
		OutLbrace()
		Output("/* XXXX Or should we use CFEqual?? */")
		Output("if ( self->ob_itself > other->ob_itself ) return 1;")
		Output("if ( self->ob_itself < other->ob_itself ) return -1;")
		Output("return 0;")
		OutRbrace()
		
	def outputHash(self):
		Output()
		Output("static int %s_hash(%s *self)", self.prefix, self.objecttype)
		OutLbrace()
		Output("/* XXXX Or should we use CFHash?? */")
		Output("return (int)self->ob_itself;")
		OutRbrace()
		
	def outputRepr(self):
		Output()
		Output("static PyObject * %s_repr(%s *self)", self.prefix, self.objecttype)
		OutLbrace()
		Output("char buf[100];")
		Output("""sprintf(buf, "<CFTypeRef type-%%d object at 0x%%08.8x for 0x%%08.8x>", CFGetTypeID(self->ob_itself), self, self->ob_itself);""")
		Output("return PyString_FromString(buf);")
		OutRbrace()

class CFTypeRefObjectDefinition(MyGlobalObjectDefinition):
	pass
	
class CFStringRefObjectDefinition(MyGlobalObjectDefinition):
	basechain = "&CFTypeRefObj_chain"
	
	def outputRepr(self):
		Output()
		Output("static PyObject * %s_repr(%s *self)", self.prefix, self.objecttype)
		OutLbrace()
		Output("char buf[100];")
		Output("""sprintf(buf, "<CFString object at 0x%%08.8x for 0x%%08.8x>", CFGetTypeID(self->ob_itself), self, self->ob_itself);""")
		Output("return PyString_FromString(buf);")
		OutRbrace()
	
# From here on it's basically all boiler plate...

# Create the generator groups and link them
module = MacModule(MODNAME, MODPREFIX, includestuff, finalstuff, initstuff)
CFTypeRef_object = CFTypeRefObjectDefinition('CFTypeRef', 'CFTypeRefObj', 'CFTypeRef')
CFStringRef_object = CFTypeRefObjectDefinition('CFStringRef', 'CFStringRefObj', 'CFStringRef')

module.addobject(CFTypeRef_object)
module.addobject(CFStringRef_object)

# Create the generator classes used to populate the lists
Function = OSErrFunctionGenerator
Method = OSErrMethodGenerator

# Create and populate the lists
functions = []
CFTypeRef_methods = []
CFStringRef_methods = []
execfile(INPUTFILE)


# add the populated lists to the generator groups
# (in a different wordl the scan program would generate this)
for f in functions: module.add(f)
for f in CFTypeRef_methods: CFTypeRef_object.add(f)
for f in CFStringRef_methods: CFStringRef_object.add(f)

# generate output (open the output file as late as possible)
SetOutputFileName(OUTPUTFILE)
module.generate()


"""Internationalization and localization support.

This module provides internationalization (I18N) and localization (L10N)
support for your Python programs by providing an interface to the GNU gettext
message catalog library.

I18N refers to the operation by which a program is made aware of multiple
languages.  L10N refers to the adaptation of your program, once
internationalized, to the local language and cultural habits.

"""

# This module represents the integration of work, contributions, feedback, and
# suggestions from the following people:
#
# Martin von Loewis, who wrote the initial implementation of the underlying
# C-based libintlmodule (later renamed _gettext), along with a skeletal
# gettext.py implementation.
#
# Peter Funk, who wrote fintl.py, a fairly complete wrapper around intlmodule,
# which also included a pure-Python implementation to read .mo files if
# intlmodule wasn't available.
#
# James Henstridge, who also wrote a gettext.py module, which has some
# interesting, but currently unsupported experimental features: the notion of
# a Catalog class and instances, and the ability to add to a catalog file via
# a Python API.
#
# Barry Warsaw integrated these modules, wrote the .install() API and code,
# and conformed all C and Python code to Python's coding standards.
#
# Francois Pinard and Marc-Andre Lemburg also contributed valuably to this
# module.
#
# J. David Ibanez implemented plural forms. Bruno Haible fixed some bugs.
#
# TODO:
# - Lazy loading of .mo files.  Currently the entire catalog is loaded into
#   memory, but that's probably bad for large translated programs.  Instead,
#   the lexical sort of original strings in GNU .mo files should be exploited
#   to do binary searches and lazy initializations.  Or you might want to use
#   the undocumented double-hash algorithm for .mo files with hash tables, but
#   you'll need to study the GNU gettext code to do this.
#
# - Support Solaris .mo file formats.  Unfortunately, we've been unable to
#   find this format documented anywhere.


import copy, os, re, struct, sys
from errno import ENOENT


__all__ = ["bindtextdomain","textdomain","gettext","dgettext",
           "find","translation","install","Catalog"]

_default_localedir = os.path.join(sys.prefix, 'share', 'locale')


def test(condition, true, false):
    """
    Implements the C expression:

      condition ? true : false

    Required to correctly interpret plural forms.
    """
    if condition:
        return true
    else:
        return false


def c2py(plural):
    """
    Gets a C expression as used in PO files for plural forms and
    returns a Python lambda function that implements an equivalent
    expression.
    """
    # Security check, allow only the "n" identifier
    from StringIO import StringIO
    import token, tokenize
    tokens = tokenize.generate_tokens(StringIO(plural).readline)
    try:
        danger = [ x for x in tokens if x[0] == token.NAME and x[1] != 'n' ]
    except tokenize.TokenError:
        raise ValueError, \
              'plural forms expression error, maybe unbalanced parenthesis'
    else:
        if danger:
            raise ValueError, 'plural forms expression could be dangerous'

    # Replace some C operators by their Python equivalents
    plural = plural.replace('&&', ' and ')
    plural = plural.replace('||', ' or ')

    expr = re.compile(r'\!([^=])')
    plural = expr.sub(' not \\1', plural)

    # Regular expression and replacement function used to transform
    # "a?b:c" to "test(a,b,c)".
    expr = re.compile(r'(.*?)\?(.*?):(.*)')
    def repl(x):
        return "test(%s, %s, %s)" % (x.group(1), x.group(2),
                                     expr.sub(repl, x.group(3)))

    # Code to transform the plural expression, taking care of parentheses
    stack = ['']
    for c in plural:
        if c == '(':
            stack.append('')
        elif c == ')':
            if len(stack) == 1:
                # Actually, we never reach this code, because unbalanced
                # parentheses get caught in the security check at the
                # beginning.
                raise ValueError, 'unbalanced parenthesis in plural form'
            s = expr.sub(repl, stack.pop())
            stack[-1] += '(%s)' % s
        else:
            stack[-1] += c
    plural = expr.sub(repl, stack.pop())

    return eval('lambda n: int(%s)' % plural)



def _expand_lang(locale):
    from locale import normalize
    locale = normalize(locale)
    COMPONENT_CODESET   = 1 << 0
    COMPONENT_TERRITORY = 1 << 1
    COMPONENT_MODIFIER  = 1 << 2
    # split up the locale into its base components
    mask = 0
    pos = locale.find('@')
    if pos >= 0:
        modifier = locale[pos:]
        locale = locale[:pos]
        mask |= COMPONENT_MODIFIER
    else:
        modifier = ''
    pos = locale.find('.')
    if pos >= 0:
        codeset = locale[pos:]
        locale = locale[:pos]
        mask |= COMPONENT_CODESET
    else:
        codeset = ''
    pos = locale.find('_')
    if pos >= 0:
        territory = locale[pos:]
        locale = locale[:pos]
        mask |= COMPONENT_TERRITORY
    else:
        territory = ''
    language = locale
    ret = []
    for i in range(mask+1):
        if not (i & ~mask):  # if all components for this combo exist ...
            val = language
            if i & COMPONENT_TERRITORY: val += territory
            if i & COMPONENT_CODESET:   val += codeset
            if i & COMPONENT_MODIFIER:  val += modifier
            ret.append(val)
    ret.reverse()
    return ret



class NullTranslations:
    def __init__(self, fp=None):
        self._info = {}
        self._charset = None
        self._fallback = None
        if fp is not None:
            self._parse(fp)

    def _parse(self, fp):
        pass

    def add_fallback(self, fallback):
        if self._fallback:
            self._fallback.add_fallback(fallback)
        else:
            self._fallback = fallback

    def gettext(self, message):
        if self._fallback:
            return self._fallback.gettext(message)
        return message

    def ngettext(self, msgid1, msgid2, n):
        if self._fallback:
            return self._fallback.ngettext(msgid1, msgid2, n)
        if n == 1:
            return msgid1
        else:
            return msgid2

    def ugettext(self, message):
        if self._fallback:
            return self._fallback.ugettext(message)
        return unicode(message)

    def ungettext(self, msgid1, msgid2, n):
        if self._fallback:
            return self._fallback.ungettext(msgid1, msgid2, n)
        if n == 1:
            return unicode(msgid1)
        else:
            return unicode(msgid2)

    def info(self):
        return self._info

    def charset(self):
        return self._charset

    def install(self, unicode=0):
        import __builtin__
        __builtin__.__dict__['_'] = unicode and self.ugettext or self.gettext


class GNUTranslations(NullTranslations):
    # Magic number of .mo files
    LE_MAGIC = 0x950412deL
    BE_MAGIC = 0xde120495L

    def _parse(self, fp):
        """Override this method to support alternative .mo formats."""
        unpack = struct.unpack
        filename = getattr(fp, 'name', '')
        # Parse the .mo file header, which consists of 5 little endian 32
        # bit words.
        self._catalog = catalog = {}
        self.plural = lambda n: int(n != 1) # germanic plural by default
        buf = fp.read()
        buflen = len(buf)
        # Are we big endian or little endian?
        magic = unpack('<I', buf[:4])[0]
        if magic == self.LE_MAGIC:
            version, msgcount, masteridx, transidx = unpack('<4I', buf[4:20])
            ii = '<II'
        elif magic == self.BE_MAGIC:
            version, msgcount, masteridx, transidx = unpack('>4I', buf[4:20])
            ii = '>II'
        else:
            raise IOError(0, 'Bad magic number', filename)
        # Now put all messages from the .mo file buffer into the catalog
        # dictionary.
        for i in xrange(0, msgcount):
            mlen, moff = unpack(ii, buf[masteridx:masteridx+8])
            mend = moff + mlen
            tlen, toff = unpack(ii, buf[transidx:transidx+8])
            tend = toff + tlen
            if mend < buflen and tend < buflen:
                msg = buf[moff:mend]
                tmsg = buf[toff:tend]
                if msg.find('\x00') >= 0:
                    # Plural forms
                    msgid1, msgid2 = msg.split('\x00')
                    tmsg = tmsg.split('\x00')
                    for i in range(len(tmsg)):
                        catalog[(msgid1, i)] = tmsg[i]
                else:
                    catalog[msg] = tmsg
            else:
                raise IOError(0, 'File is corrupt', filename)
            # See if we're looking at GNU .mo conventions for metadata
            if mlen == 0:
                # Catalog description
                for item in tmsg.split('\n'):
                    item = item.strip()
                    if not item:
                        continue
                    k, v = item.split(':', 1)
                    k = k.strip().lower()
                    v = v.strip()
                    self._info[k] = v
                    if k == 'content-type':
                        self._charset = v.split('charset=')[1]
                    elif k == 'plural-forms':
                        v = v.split(';')
##                        nplurals = v[0].split('nplurals=')[1]
##                        nplurals = int(nplurals.strip())
                        plural = v[1].split('plural=')[1]
                        self.plural = c2py(plural)
            # advance to next entry in the seek tables
            masteridx += 8
            transidx += 8

    def gettext(self, message):
        try:
            return self._catalog[message]
        except KeyError:
            if self._fallback:
                return self._fallback.gettext(message)
            return message


    def ngettext(self, msgid1, msgid2, n):
        try:
            return self._catalog[(msgid1, self.plural(n))]
        except KeyError:
            if self._fallback:
                return self._fallback.ngettext(msgid1, msgid2, n)
            if n == 1:
                return msgid1
            else:
                return msgid2


    def ugettext(self, message):
        try:
            tmsg = self._catalog[message]
        except KeyError:
            if self._fallback:
                return self._fallback.ugettext(message)
            tmsg = message
        return unicode(tmsg, self._charset)


    def ungettext(self, msgid1, msgid2, n):
        try:
            tmsg = self._catalog[(msgid1, self.plural(n))]
        except KeyError:
            if self._fallback:
                return self._fallback.ungettext(msgid1, msgid2, n)
            if n == 1:
                tmsg = msgid1
            else:
                tmsg = msgid2
        return unicode(tmsg, self._charset)


# Locate a .mo file using the gettext strategy
def find(domain, localedir=None, languages=None, all=0):
    # Get some reasonable defaults for arguments that were not supplied
    if localedir is None:
        localedir = _default_localedir
    if languages is None:
        languages = []
        for envar in ('LANGUAGE', 'LC_ALL', 'LC_MESSAGES', 'LANG'):
            val = os.environ.get(envar)
            if val:
                languages = val.split(':')
                break
        if 'C' not in languages:
            languages.append('C')
    # now normalize and expand the languages
    nelangs = []
    for lang in languages:
        for nelang in _expand_lang(lang):
            if nelang not in nelangs:
                nelangs.append(nelang)
    # select a language
    if all:
        result = []
    else:
        result = None
    for lang in nelangs:
        if lang == 'C':
            break
        mofile = os.path.join(localedir, lang, 'LC_MESSAGES', '%s.mo' % domain)
        if os.path.exists(mofile):
            if all:
                result.append(mofile)
            else:
                return mofile
    return result



# a mapping between absolute .mo file path and Translation object
_translations = {}

def translation(domain, localedir=None, languages=None,
                class_=None, fallback=0):
    if class_ is None:
        class_ = GNUTranslations
    mofiles = find(domain, localedir, languages, all=1)
    if len(mofiles)==0:
        if fallback:
            return NullTranslations()
        raise IOError(ENOENT, 'No translation file found for domain', domain)
    # TBD: do we need to worry about the file pointer getting collected?
    # Avoid opening, reading, and parsing the .mo file after it's been done
    # once.
    result = None
    for mofile in mofiles:
        key = os.path.abspath(mofile)
        t = _translations.get(key)
        if t is None:
            t = _translations.setdefault(key, class_(open(mofile, 'rb')))
        # Copy the translation object to allow setting fallbacks.
        # All other instance data is shared with the cached object.
        t = copy.copy(t)
        if result is None:
            result = t
        else:
            result.add_fallback(t)
    return result


def install(domain, localedir=None, unicode=0):
    translation(domain, localedir, fallback=1).install(unicode)



# a mapping b/w domains and locale directories
_localedirs = {}
# current global domain, `messages' used for compatibility w/ GNU gettext
_current_domain = 'messages'


def textdomain(domain=None):
    global _current_domain
    if domain is not None:
        _current_domain = domain
    return _current_domain


def bindtextdomain(domain, localedir=None):
    global _localedirs
    if localedir is not None:
        _localedirs[domain] = localedir
    return _localedirs.get(domain, _default_localedir)


def dgettext(domain, message):
    try:
        t = translation(domain, _localedirs.get(domain, None))
    except IOError:
        return message
    return t.gettext(message)


def dngettext(domain, msgid1, msgid2, n):
    try:
        t = translation(domain, _localedirs.get(domain, None))
    except IOError:
        if n == 1:
            return msgid1
        else:
            return msgid2
    return t.ngettext(msgid1, msgid2, n)


def gettext(message):
    return dgettext(_current_domain, message)


def ngettext(msgid1, msgid2, n):
    return dngettext(_current_domain, msgid1, msgid2, n)


# dcgettext() has been deemed unnecessary and is not implemented.

# James Henstridge's Catalog constructor from GNOME gettext.  Documented usage
# was:
#
#    import gettext
#    cat = gettext.Catalog(PACKAGE, localedir=LOCALEDIR)
#    _ = cat.gettext
#    print _('Hello World')

# The resulting catalog object currently don't support access through a
# dictionary API, which was supported (but apparently unused) in GNOME
# gettext.

Catalog = translation

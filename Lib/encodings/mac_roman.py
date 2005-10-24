""" Python Character Mapping Codec generated from 'MAPPINGS/VENDORS/APPLE/ROMAN.TXT' with gencodec.py.

"""#"

import codecs

### Codec APIs

class Codec(codecs.Codec):

    def encode(self,input,errors='strict'):

        return codecs.charmap_encode(input,errors,encoding_map)

    def decode(self,input,errors='strict'):

        return codecs.charmap_decode(input,errors,decoding_table)
    
class StreamWriter(Codec,codecs.StreamWriter):
    pass

class StreamReader(Codec,codecs.StreamReader):
    pass

### encodings module API

def getregentry():

    return (Codec().encode,Codec().decode,StreamReader,StreamWriter)


### Decoding Table

decoding_table = (
    u'\x00'	#  0x00 -> CONTROL CHARACTER
    u'\x01'	#  0x01 -> CONTROL CHARACTER
    u'\x02'	#  0x02 -> CONTROL CHARACTER
    u'\x03'	#  0x03 -> CONTROL CHARACTER
    u'\x04'	#  0x04 -> CONTROL CHARACTER
    u'\x05'	#  0x05 -> CONTROL CHARACTER
    u'\x06'	#  0x06 -> CONTROL CHARACTER
    u'\x07'	#  0x07 -> CONTROL CHARACTER
    u'\x08'	#  0x08 -> CONTROL CHARACTER
    u'\t'	#  0x09 -> CONTROL CHARACTER
    u'\n'	#  0x0a -> CONTROL CHARACTER
    u'\x0b'	#  0x0b -> CONTROL CHARACTER
    u'\x0c'	#  0x0c -> CONTROL CHARACTER
    u'\r'	#  0x0d -> CONTROL CHARACTER
    u'\x0e'	#  0x0e -> CONTROL CHARACTER
    u'\x0f'	#  0x0f -> CONTROL CHARACTER
    u'\x10'	#  0x10 -> CONTROL CHARACTER
    u'\x11'	#  0x11 -> CONTROL CHARACTER
    u'\x12'	#  0x12 -> CONTROL CHARACTER
    u'\x13'	#  0x13 -> CONTROL CHARACTER
    u'\x14'	#  0x14 -> CONTROL CHARACTER
    u'\x15'	#  0x15 -> CONTROL CHARACTER
    u'\x16'	#  0x16 -> CONTROL CHARACTER
    u'\x17'	#  0x17 -> CONTROL CHARACTER
    u'\x18'	#  0x18 -> CONTROL CHARACTER
    u'\x19'	#  0x19 -> CONTROL CHARACTER
    u'\x1a'	#  0x1a -> CONTROL CHARACTER
    u'\x1b'	#  0x1b -> CONTROL CHARACTER
    u'\x1c'	#  0x1c -> CONTROL CHARACTER
    u'\x1d'	#  0x1d -> CONTROL CHARACTER
    u'\x1e'	#  0x1e -> CONTROL CHARACTER
    u'\x1f'	#  0x1f -> CONTROL CHARACTER
    u' '	#  0x20 -> SPACE
    u'!'	#  0x21 -> EXCLAMATION MARK
    u'"'	#  0x22 -> QUOTATION MARK
    u'#'	#  0x23 -> NUMBER SIGN
    u'$'	#  0x24 -> DOLLAR SIGN
    u'%'	#  0x25 -> PERCENT SIGN
    u'&'	#  0x26 -> AMPERSAND
    u"'"	#  0x27 -> APOSTROPHE
    u'('	#  0x28 -> LEFT PARENTHESIS
    u')'	#  0x29 -> RIGHT PARENTHESIS
    u'*'	#  0x2a -> ASTERISK
    u'+'	#  0x2b -> PLUS SIGN
    u','	#  0x2c -> COMMA
    u'-'	#  0x2d -> HYPHEN-MINUS
    u'.'	#  0x2e -> FULL STOP
    u'/'	#  0x2f -> SOLIDUS
    u'0'	#  0x30 -> DIGIT ZERO
    u'1'	#  0x31 -> DIGIT ONE
    u'2'	#  0x32 -> DIGIT TWO
    u'3'	#  0x33 -> DIGIT THREE
    u'4'	#  0x34 -> DIGIT FOUR
    u'5'	#  0x35 -> DIGIT FIVE
    u'6'	#  0x36 -> DIGIT SIX
    u'7'	#  0x37 -> DIGIT SEVEN
    u'8'	#  0x38 -> DIGIT EIGHT
    u'9'	#  0x39 -> DIGIT NINE
    u':'	#  0x3a -> COLON
    u';'	#  0x3b -> SEMICOLON
    u'<'	#  0x3c -> LESS-THAN SIGN
    u'='	#  0x3d -> EQUALS SIGN
    u'>'	#  0x3e -> GREATER-THAN SIGN
    u'?'	#  0x3f -> QUESTION MARK
    u'@'	#  0x40 -> COMMERCIAL AT
    u'A'	#  0x41 -> LATIN CAPITAL LETTER A
    u'B'	#  0x42 -> LATIN CAPITAL LETTER B
    u'C'	#  0x43 -> LATIN CAPITAL LETTER C
    u'D'	#  0x44 -> LATIN CAPITAL LETTER D
    u'E'	#  0x45 -> LATIN CAPITAL LETTER E
    u'F'	#  0x46 -> LATIN CAPITAL LETTER F
    u'G'	#  0x47 -> LATIN CAPITAL LETTER G
    u'H'	#  0x48 -> LATIN CAPITAL LETTER H
    u'I'	#  0x49 -> LATIN CAPITAL LETTER I
    u'J'	#  0x4a -> LATIN CAPITAL LETTER J
    u'K'	#  0x4b -> LATIN CAPITAL LETTER K
    u'L'	#  0x4c -> LATIN CAPITAL LETTER L
    u'M'	#  0x4d -> LATIN CAPITAL LETTER M
    u'N'	#  0x4e -> LATIN CAPITAL LETTER N
    u'O'	#  0x4f -> LATIN CAPITAL LETTER O
    u'P'	#  0x50 -> LATIN CAPITAL LETTER P
    u'Q'	#  0x51 -> LATIN CAPITAL LETTER Q
    u'R'	#  0x52 -> LATIN CAPITAL LETTER R
    u'S'	#  0x53 -> LATIN CAPITAL LETTER S
    u'T'	#  0x54 -> LATIN CAPITAL LETTER T
    u'U'	#  0x55 -> LATIN CAPITAL LETTER U
    u'V'	#  0x56 -> LATIN CAPITAL LETTER V
    u'W'	#  0x57 -> LATIN CAPITAL LETTER W
    u'X'	#  0x58 -> LATIN CAPITAL LETTER X
    u'Y'	#  0x59 -> LATIN CAPITAL LETTER Y
    u'Z'	#  0x5a -> LATIN CAPITAL LETTER Z
    u'['	#  0x5b -> LEFT SQUARE BRACKET
    u'\\'	#  0x5c -> REVERSE SOLIDUS
    u']'	#  0x5d -> RIGHT SQUARE BRACKET
    u'^'	#  0x5e -> CIRCUMFLEX ACCENT
    u'_'	#  0x5f -> LOW LINE
    u'`'	#  0x60 -> GRAVE ACCENT
    u'a'	#  0x61 -> LATIN SMALL LETTER A
    u'b'	#  0x62 -> LATIN SMALL LETTER B
    u'c'	#  0x63 -> LATIN SMALL LETTER C
    u'd'	#  0x64 -> LATIN SMALL LETTER D
    u'e'	#  0x65 -> LATIN SMALL LETTER E
    u'f'	#  0x66 -> LATIN SMALL LETTER F
    u'g'	#  0x67 -> LATIN SMALL LETTER G
    u'h'	#  0x68 -> LATIN SMALL LETTER H
    u'i'	#  0x69 -> LATIN SMALL LETTER I
    u'j'	#  0x6a -> LATIN SMALL LETTER J
    u'k'	#  0x6b -> LATIN SMALL LETTER K
    u'l'	#  0x6c -> LATIN SMALL LETTER L
    u'm'	#  0x6d -> LATIN SMALL LETTER M
    u'n'	#  0x6e -> LATIN SMALL LETTER N
    u'o'	#  0x6f -> LATIN SMALL LETTER O
    u'p'	#  0x70 -> LATIN SMALL LETTER P
    u'q'	#  0x71 -> LATIN SMALL LETTER Q
    u'r'	#  0x72 -> LATIN SMALL LETTER R
    u's'	#  0x73 -> LATIN SMALL LETTER S
    u't'	#  0x74 -> LATIN SMALL LETTER T
    u'u'	#  0x75 -> LATIN SMALL LETTER U
    u'v'	#  0x76 -> LATIN SMALL LETTER V
    u'w'	#  0x77 -> LATIN SMALL LETTER W
    u'x'	#  0x78 -> LATIN SMALL LETTER X
    u'y'	#  0x79 -> LATIN SMALL LETTER Y
    u'z'	#  0x7a -> LATIN SMALL LETTER Z
    u'{'	#  0x7b -> LEFT CURLY BRACKET
    u'|'	#  0x7c -> VERTICAL LINE
    u'}'	#  0x7d -> RIGHT CURLY BRACKET
    u'~'	#  0x7e -> TILDE
    u'\x7f'	#  0x7f -> CONTROL CHARACTER
    u'\xc4'	#  0x80 -> LATIN CAPITAL LETTER A WITH DIAERESIS
    u'\xc5'	#  0x81 -> LATIN CAPITAL LETTER A WITH RING ABOVE
    u'\xc7'	#  0x82 -> LATIN CAPITAL LETTER C WITH CEDILLA
    u'\xc9'	#  0x83 -> LATIN CAPITAL LETTER E WITH ACUTE
    u'\xd1'	#  0x84 -> LATIN CAPITAL LETTER N WITH TILDE
    u'\xd6'	#  0x85 -> LATIN CAPITAL LETTER O WITH DIAERESIS
    u'\xdc'	#  0x86 -> LATIN CAPITAL LETTER U WITH DIAERESIS
    u'\xe1'	#  0x87 -> LATIN SMALL LETTER A WITH ACUTE
    u'\xe0'	#  0x88 -> LATIN SMALL LETTER A WITH GRAVE
    u'\xe2'	#  0x89 -> LATIN SMALL LETTER A WITH CIRCUMFLEX
    u'\xe4'	#  0x8a -> LATIN SMALL LETTER A WITH DIAERESIS
    u'\xe3'	#  0x8b -> LATIN SMALL LETTER A WITH TILDE
    u'\xe5'	#  0x8c -> LATIN SMALL LETTER A WITH RING ABOVE
    u'\xe7'	#  0x8d -> LATIN SMALL LETTER C WITH CEDILLA
    u'\xe9'	#  0x8e -> LATIN SMALL LETTER E WITH ACUTE
    u'\xe8'	#  0x8f -> LATIN SMALL LETTER E WITH GRAVE
    u'\xea'	#  0x90 -> LATIN SMALL LETTER E WITH CIRCUMFLEX
    u'\xeb'	#  0x91 -> LATIN SMALL LETTER E WITH DIAERESIS
    u'\xed'	#  0x92 -> LATIN SMALL LETTER I WITH ACUTE
    u'\xec'	#  0x93 -> LATIN SMALL LETTER I WITH GRAVE
    u'\xee'	#  0x94 -> LATIN SMALL LETTER I WITH CIRCUMFLEX
    u'\xef'	#  0x95 -> LATIN SMALL LETTER I WITH DIAERESIS
    u'\xf1'	#  0x96 -> LATIN SMALL LETTER N WITH TILDE
    u'\xf3'	#  0x97 -> LATIN SMALL LETTER O WITH ACUTE
    u'\xf2'	#  0x98 -> LATIN SMALL LETTER O WITH GRAVE
    u'\xf4'	#  0x99 -> LATIN SMALL LETTER O WITH CIRCUMFLEX
    u'\xf6'	#  0x9a -> LATIN SMALL LETTER O WITH DIAERESIS
    u'\xf5'	#  0x9b -> LATIN SMALL LETTER O WITH TILDE
    u'\xfa'	#  0x9c -> LATIN SMALL LETTER U WITH ACUTE
    u'\xf9'	#  0x9d -> LATIN SMALL LETTER U WITH GRAVE
    u'\xfb'	#  0x9e -> LATIN SMALL LETTER U WITH CIRCUMFLEX
    u'\xfc'	#  0x9f -> LATIN SMALL LETTER U WITH DIAERESIS
    u'\u2020'	#  0xa0 -> DAGGER
    u'\xb0'	#  0xa1 -> DEGREE SIGN
    u'\xa2'	#  0xa2 -> CENT SIGN
    u'\xa3'	#  0xa3 -> POUND SIGN
    u'\xa7'	#  0xa4 -> SECTION SIGN
    u'\u2022'	#  0xa5 -> BULLET
    u'\xb6'	#  0xa6 -> PILCROW SIGN
    u'\xdf'	#  0xa7 -> LATIN SMALL LETTER SHARP S
    u'\xae'	#  0xa8 -> REGISTERED SIGN
    u'\xa9'	#  0xa9 -> COPYRIGHT SIGN
    u'\u2122'	#  0xaa -> TRADE MARK SIGN
    u'\xb4'	#  0xab -> ACUTE ACCENT
    u'\xa8'	#  0xac -> DIAERESIS
    u'\u2260'	#  0xad -> NOT EQUAL TO
    u'\xc6'	#  0xae -> LATIN CAPITAL LETTER AE
    u'\xd8'	#  0xaf -> LATIN CAPITAL LETTER O WITH STROKE
    u'\u221e'	#  0xb0 -> INFINITY
    u'\xb1'	#  0xb1 -> PLUS-MINUS SIGN
    u'\u2264'	#  0xb2 -> LESS-THAN OR EQUAL TO
    u'\u2265'	#  0xb3 -> GREATER-THAN OR EQUAL TO
    u'\xa5'	#  0xb4 -> YEN SIGN
    u'\xb5'	#  0xb5 -> MICRO SIGN
    u'\u2202'	#  0xb6 -> PARTIAL DIFFERENTIAL
    u'\u2211'	#  0xb7 -> N-ARY SUMMATION
    u'\u220f'	#  0xb8 -> N-ARY PRODUCT
    u'\u03c0'	#  0xb9 -> GREEK SMALL LETTER PI
    u'\u222b'	#  0xba -> INTEGRAL
    u'\xaa'	#  0xbb -> FEMININE ORDINAL INDICATOR
    u'\xba'	#  0xbc -> MASCULINE ORDINAL INDICATOR
    u'\u03a9'	#  0xbd -> GREEK CAPITAL LETTER OMEGA
    u'\xe6'	#  0xbe -> LATIN SMALL LETTER AE
    u'\xf8'	#  0xbf -> LATIN SMALL LETTER O WITH STROKE
    u'\xbf'	#  0xc0 -> INVERTED QUESTION MARK
    u'\xa1'	#  0xc1 -> INVERTED EXCLAMATION MARK
    u'\xac'	#  0xc2 -> NOT SIGN
    u'\u221a'	#  0xc3 -> SQUARE ROOT
    u'\u0192'	#  0xc4 -> LATIN SMALL LETTER F WITH HOOK
    u'\u2248'	#  0xc5 -> ALMOST EQUAL TO
    u'\u2206'	#  0xc6 -> INCREMENT
    u'\xab'	#  0xc7 -> LEFT-POINTING DOUBLE ANGLE QUOTATION MARK
    u'\xbb'	#  0xc8 -> RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK
    u'\u2026'	#  0xc9 -> HORIZONTAL ELLIPSIS
    u'\xa0'	#  0xca -> NO-BREAK SPACE
    u'\xc0'	#  0xcb -> LATIN CAPITAL LETTER A WITH GRAVE
    u'\xc3'	#  0xcc -> LATIN CAPITAL LETTER A WITH TILDE
    u'\xd5'	#  0xcd -> LATIN CAPITAL LETTER O WITH TILDE
    u'\u0152'	#  0xce -> LATIN CAPITAL LIGATURE OE
    u'\u0153'	#  0xcf -> LATIN SMALL LIGATURE OE
    u'\u2013'	#  0xd0 -> EN DASH
    u'\u2014'	#  0xd1 -> EM DASH
    u'\u201c'	#  0xd2 -> LEFT DOUBLE QUOTATION MARK
    u'\u201d'	#  0xd3 -> RIGHT DOUBLE QUOTATION MARK
    u'\u2018'	#  0xd4 -> LEFT SINGLE QUOTATION MARK
    u'\u2019'	#  0xd5 -> RIGHT SINGLE QUOTATION MARK
    u'\xf7'	#  0xd6 -> DIVISION SIGN
    u'\u25ca'	#  0xd7 -> LOZENGE
    u'\xff'	#  0xd8 -> LATIN SMALL LETTER Y WITH DIAERESIS
    u'\u0178'	#  0xd9 -> LATIN CAPITAL LETTER Y WITH DIAERESIS
    u'\u2044'	#  0xda -> FRACTION SLASH
    u'\u20ac'	#  0xdb -> EURO SIGN
    u'\u2039'	#  0xdc -> SINGLE LEFT-POINTING ANGLE QUOTATION MARK
    u'\u203a'	#  0xdd -> SINGLE RIGHT-POINTING ANGLE QUOTATION MARK
    u'\ufb01'	#  0xde -> LATIN SMALL LIGATURE FI
    u'\ufb02'	#  0xdf -> LATIN SMALL LIGATURE FL
    u'\u2021'	#  0xe0 -> DOUBLE DAGGER
    u'\xb7'	#  0xe1 -> MIDDLE DOT
    u'\u201a'	#  0xe2 -> SINGLE LOW-9 QUOTATION MARK
    u'\u201e'	#  0xe3 -> DOUBLE LOW-9 QUOTATION MARK
    u'\u2030'	#  0xe4 -> PER MILLE SIGN
    u'\xc2'	#  0xe5 -> LATIN CAPITAL LETTER A WITH CIRCUMFLEX
    u'\xca'	#  0xe6 -> LATIN CAPITAL LETTER E WITH CIRCUMFLEX
    u'\xc1'	#  0xe7 -> LATIN CAPITAL LETTER A WITH ACUTE
    u'\xcb'	#  0xe8 -> LATIN CAPITAL LETTER E WITH DIAERESIS
    u'\xc8'	#  0xe9 -> LATIN CAPITAL LETTER E WITH GRAVE
    u'\xcd'	#  0xea -> LATIN CAPITAL LETTER I WITH ACUTE
    u'\xce'	#  0xeb -> LATIN CAPITAL LETTER I WITH CIRCUMFLEX
    u'\xcf'	#  0xec -> LATIN CAPITAL LETTER I WITH DIAERESIS
    u'\xcc'	#  0xed -> LATIN CAPITAL LETTER I WITH GRAVE
    u'\xd3'	#  0xee -> LATIN CAPITAL LETTER O WITH ACUTE
    u'\xd4'	#  0xef -> LATIN CAPITAL LETTER O WITH CIRCUMFLEX
    u'\uf8ff'	#  0xf0 -> Apple logo
    u'\xd2'	#  0xf1 -> LATIN CAPITAL LETTER O WITH GRAVE
    u'\xda'	#  0xf2 -> LATIN CAPITAL LETTER U WITH ACUTE
    u'\xdb'	#  0xf3 -> LATIN CAPITAL LETTER U WITH CIRCUMFLEX
    u'\xd9'	#  0xf4 -> LATIN CAPITAL LETTER U WITH GRAVE
    u'\u0131'	#  0xf5 -> LATIN SMALL LETTER DOTLESS I
    u'\u02c6'	#  0xf6 -> MODIFIER LETTER CIRCUMFLEX ACCENT
    u'\u02dc'	#  0xf7 -> SMALL TILDE
    u'\xaf'	#  0xf8 -> MACRON
    u'\u02d8'	#  0xf9 -> BREVE
    u'\u02d9'	#  0xfa -> DOT ABOVE
    u'\u02da'	#  0xfb -> RING ABOVE
    u'\xb8'	#  0xfc -> CEDILLA
    u'\u02dd'	#  0xfd -> DOUBLE ACUTE ACCENT
    u'\u02db'	#  0xfe -> OGONEK
    u'\u02c7'	#  0xff -> CARON
)

### Encoding Map

encoding_map = {
    0x0000: 0x00,	#  CONTROL CHARACTER
    0x0001: 0x01,	#  CONTROL CHARACTER
    0x0002: 0x02,	#  CONTROL CHARACTER
    0x0003: 0x03,	#  CONTROL CHARACTER
    0x0004: 0x04,	#  CONTROL CHARACTER
    0x0005: 0x05,	#  CONTROL CHARACTER
    0x0006: 0x06,	#  CONTROL CHARACTER
    0x0007: 0x07,	#  CONTROL CHARACTER
    0x0008: 0x08,	#  CONTROL CHARACTER
    0x0009: 0x09,	#  CONTROL CHARACTER
    0x000a: 0x0a,	#  CONTROL CHARACTER
    0x000b: 0x0b,	#  CONTROL CHARACTER
    0x000c: 0x0c,	#  CONTROL CHARACTER
    0x000d: 0x0d,	#  CONTROL CHARACTER
    0x000e: 0x0e,	#  CONTROL CHARACTER
    0x000f: 0x0f,	#  CONTROL CHARACTER
    0x0010: 0x10,	#  CONTROL CHARACTER
    0x0011: 0x11,	#  CONTROL CHARACTER
    0x0012: 0x12,	#  CONTROL CHARACTER
    0x0013: 0x13,	#  CONTROL CHARACTER
    0x0014: 0x14,	#  CONTROL CHARACTER
    0x0015: 0x15,	#  CONTROL CHARACTER
    0x0016: 0x16,	#  CONTROL CHARACTER
    0x0017: 0x17,	#  CONTROL CHARACTER
    0x0018: 0x18,	#  CONTROL CHARACTER
    0x0019: 0x19,	#  CONTROL CHARACTER
    0x001a: 0x1a,	#  CONTROL CHARACTER
    0x001b: 0x1b,	#  CONTROL CHARACTER
    0x001c: 0x1c,	#  CONTROL CHARACTER
    0x001d: 0x1d,	#  CONTROL CHARACTER
    0x001e: 0x1e,	#  CONTROL CHARACTER
    0x001f: 0x1f,	#  CONTROL CHARACTER
    0x0020: 0x20,	#  SPACE
    0x0021: 0x21,	#  EXCLAMATION MARK
    0x0022: 0x22,	#  QUOTATION MARK
    0x0023: 0x23,	#  NUMBER SIGN
    0x0024: 0x24,	#  DOLLAR SIGN
    0x0025: 0x25,	#  PERCENT SIGN
    0x0026: 0x26,	#  AMPERSAND
    0x0027: 0x27,	#  APOSTROPHE
    0x0028: 0x28,	#  LEFT PARENTHESIS
    0x0029: 0x29,	#  RIGHT PARENTHESIS
    0x002a: 0x2a,	#  ASTERISK
    0x002b: 0x2b,	#  PLUS SIGN
    0x002c: 0x2c,	#  COMMA
    0x002d: 0x2d,	#  HYPHEN-MINUS
    0x002e: 0x2e,	#  FULL STOP
    0x002f: 0x2f,	#  SOLIDUS
    0x0030: 0x30,	#  DIGIT ZERO
    0x0031: 0x31,	#  DIGIT ONE
    0x0032: 0x32,	#  DIGIT TWO
    0x0033: 0x33,	#  DIGIT THREE
    0x0034: 0x34,	#  DIGIT FOUR
    0x0035: 0x35,	#  DIGIT FIVE
    0x0036: 0x36,	#  DIGIT SIX
    0x0037: 0x37,	#  DIGIT SEVEN
    0x0038: 0x38,	#  DIGIT EIGHT
    0x0039: 0x39,	#  DIGIT NINE
    0x003a: 0x3a,	#  COLON
    0x003b: 0x3b,	#  SEMICOLON
    0x003c: 0x3c,	#  LESS-THAN SIGN
    0x003d: 0x3d,	#  EQUALS SIGN
    0x003e: 0x3e,	#  GREATER-THAN SIGN
    0x003f: 0x3f,	#  QUESTION MARK
    0x0040: 0x40,	#  COMMERCIAL AT
    0x0041: 0x41,	#  LATIN CAPITAL LETTER A
    0x0042: 0x42,	#  LATIN CAPITAL LETTER B
    0x0043: 0x43,	#  LATIN CAPITAL LETTER C
    0x0044: 0x44,	#  LATIN CAPITAL LETTER D
    0x0045: 0x45,	#  LATIN CAPITAL LETTER E
    0x0046: 0x46,	#  LATIN CAPITAL LETTER F
    0x0047: 0x47,	#  LATIN CAPITAL LETTER G
    0x0048: 0x48,	#  LATIN CAPITAL LETTER H
    0x0049: 0x49,	#  LATIN CAPITAL LETTER I
    0x004a: 0x4a,	#  LATIN CAPITAL LETTER J
    0x004b: 0x4b,	#  LATIN CAPITAL LETTER K
    0x004c: 0x4c,	#  LATIN CAPITAL LETTER L
    0x004d: 0x4d,	#  LATIN CAPITAL LETTER M
    0x004e: 0x4e,	#  LATIN CAPITAL LETTER N
    0x004f: 0x4f,	#  LATIN CAPITAL LETTER O
    0x0050: 0x50,	#  LATIN CAPITAL LETTER P
    0x0051: 0x51,	#  LATIN CAPITAL LETTER Q
    0x0052: 0x52,	#  LATIN CAPITAL LETTER R
    0x0053: 0x53,	#  LATIN CAPITAL LETTER S
    0x0054: 0x54,	#  LATIN CAPITAL LETTER T
    0x0055: 0x55,	#  LATIN CAPITAL LETTER U
    0x0056: 0x56,	#  LATIN CAPITAL LETTER V
    0x0057: 0x57,	#  LATIN CAPITAL LETTER W
    0x0058: 0x58,	#  LATIN CAPITAL LETTER X
    0x0059: 0x59,	#  LATIN CAPITAL LETTER Y
    0x005a: 0x5a,	#  LATIN CAPITAL LETTER Z
    0x005b: 0x5b,	#  LEFT SQUARE BRACKET
    0x005c: 0x5c,	#  REVERSE SOLIDUS
    0x005d: 0x5d,	#  RIGHT SQUARE BRACKET
    0x005e: 0x5e,	#  CIRCUMFLEX ACCENT
    0x005f: 0x5f,	#  LOW LINE
    0x0060: 0x60,	#  GRAVE ACCENT
    0x0061: 0x61,	#  LATIN SMALL LETTER A
    0x0062: 0x62,	#  LATIN SMALL LETTER B
    0x0063: 0x63,	#  LATIN SMALL LETTER C
    0x0064: 0x64,	#  LATIN SMALL LETTER D
    0x0065: 0x65,	#  LATIN SMALL LETTER E
    0x0066: 0x66,	#  LATIN SMALL LETTER F
    0x0067: 0x67,	#  LATIN SMALL LETTER G
    0x0068: 0x68,	#  LATIN SMALL LETTER H
    0x0069: 0x69,	#  LATIN SMALL LETTER I
    0x006a: 0x6a,	#  LATIN SMALL LETTER J
    0x006b: 0x6b,	#  LATIN SMALL LETTER K
    0x006c: 0x6c,	#  LATIN SMALL LETTER L
    0x006d: 0x6d,	#  LATIN SMALL LETTER M
    0x006e: 0x6e,	#  LATIN SMALL LETTER N
    0x006f: 0x6f,	#  LATIN SMALL LETTER O
    0x0070: 0x70,	#  LATIN SMALL LETTER P
    0x0071: 0x71,	#  LATIN SMALL LETTER Q
    0x0072: 0x72,	#  LATIN SMALL LETTER R
    0x0073: 0x73,	#  LATIN SMALL LETTER S
    0x0074: 0x74,	#  LATIN SMALL LETTER T
    0x0075: 0x75,	#  LATIN SMALL LETTER U
    0x0076: 0x76,	#  LATIN SMALL LETTER V
    0x0077: 0x77,	#  LATIN SMALL LETTER W
    0x0078: 0x78,	#  LATIN SMALL LETTER X
    0x0079: 0x79,	#  LATIN SMALL LETTER Y
    0x007a: 0x7a,	#  LATIN SMALL LETTER Z
    0x007b: 0x7b,	#  LEFT CURLY BRACKET
    0x007c: 0x7c,	#  VERTICAL LINE
    0x007d: 0x7d,	#  RIGHT CURLY BRACKET
    0x007e: 0x7e,	#  TILDE
    0x007f: 0x7f,	#  CONTROL CHARACTER
    0x00a0: 0xca,	#  NO-BREAK SPACE
    0x00a1: 0xc1,	#  INVERTED EXCLAMATION MARK
    0x00a2: 0xa2,	#  CENT SIGN
    0x00a3: 0xa3,	#  POUND SIGN
    0x00a5: 0xb4,	#  YEN SIGN
    0x00a7: 0xa4,	#  SECTION SIGN
    0x00a8: 0xac,	#  DIAERESIS
    0x00a9: 0xa9,	#  COPYRIGHT SIGN
    0x00aa: 0xbb,	#  FEMININE ORDINAL INDICATOR
    0x00ab: 0xc7,	#  LEFT-POINTING DOUBLE ANGLE QUOTATION MARK
    0x00ac: 0xc2,	#  NOT SIGN
    0x00ae: 0xa8,	#  REGISTERED SIGN
    0x00af: 0xf8,	#  MACRON
    0x00b0: 0xa1,	#  DEGREE SIGN
    0x00b1: 0xb1,	#  PLUS-MINUS SIGN
    0x00b4: 0xab,	#  ACUTE ACCENT
    0x00b5: 0xb5,	#  MICRO SIGN
    0x00b6: 0xa6,	#  PILCROW SIGN
    0x00b7: 0xe1,	#  MIDDLE DOT
    0x00b8: 0xfc,	#  CEDILLA
    0x00ba: 0xbc,	#  MASCULINE ORDINAL INDICATOR
    0x00bb: 0xc8,	#  RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK
    0x00bf: 0xc0,	#  INVERTED QUESTION MARK
    0x00c0: 0xcb,	#  LATIN CAPITAL LETTER A WITH GRAVE
    0x00c1: 0xe7,	#  LATIN CAPITAL LETTER A WITH ACUTE
    0x00c2: 0xe5,	#  LATIN CAPITAL LETTER A WITH CIRCUMFLEX
    0x00c3: 0xcc,	#  LATIN CAPITAL LETTER A WITH TILDE
    0x00c4: 0x80,	#  LATIN CAPITAL LETTER A WITH DIAERESIS
    0x00c5: 0x81,	#  LATIN CAPITAL LETTER A WITH RING ABOVE
    0x00c6: 0xae,	#  LATIN CAPITAL LETTER AE
    0x00c7: 0x82,	#  LATIN CAPITAL LETTER C WITH CEDILLA
    0x00c8: 0xe9,	#  LATIN CAPITAL LETTER E WITH GRAVE
    0x00c9: 0x83,	#  LATIN CAPITAL LETTER E WITH ACUTE
    0x00ca: 0xe6,	#  LATIN CAPITAL LETTER E WITH CIRCUMFLEX
    0x00cb: 0xe8,	#  LATIN CAPITAL LETTER E WITH DIAERESIS
    0x00cc: 0xed,	#  LATIN CAPITAL LETTER I WITH GRAVE
    0x00cd: 0xea,	#  LATIN CAPITAL LETTER I WITH ACUTE
    0x00ce: 0xeb,	#  LATIN CAPITAL LETTER I WITH CIRCUMFLEX
    0x00cf: 0xec,	#  LATIN CAPITAL LETTER I WITH DIAERESIS
    0x00d1: 0x84,	#  LATIN CAPITAL LETTER N WITH TILDE
    0x00d2: 0xf1,	#  LATIN CAPITAL LETTER O WITH GRAVE
    0x00d3: 0xee,	#  LATIN CAPITAL LETTER O WITH ACUTE
    0x00d4: 0xef,	#  LATIN CAPITAL LETTER O WITH CIRCUMFLEX
    0x00d5: 0xcd,	#  LATIN CAPITAL LETTER O WITH TILDE
    0x00d6: 0x85,	#  LATIN CAPITAL LETTER O WITH DIAERESIS
    0x00d8: 0xaf,	#  LATIN CAPITAL LETTER O WITH STROKE
    0x00d9: 0xf4,	#  LATIN CAPITAL LETTER U WITH GRAVE
    0x00da: 0xf2,	#  LATIN CAPITAL LETTER U WITH ACUTE
    0x00db: 0xf3,	#  LATIN CAPITAL LETTER U WITH CIRCUMFLEX
    0x00dc: 0x86,	#  LATIN CAPITAL LETTER U WITH DIAERESIS
    0x00df: 0xa7,	#  LATIN SMALL LETTER SHARP S
    0x00e0: 0x88,	#  LATIN SMALL LETTER A WITH GRAVE
    0x00e1: 0x87,	#  LATIN SMALL LETTER A WITH ACUTE
    0x00e2: 0x89,	#  LATIN SMALL LETTER A WITH CIRCUMFLEX
    0x00e3: 0x8b,	#  LATIN SMALL LETTER A WITH TILDE
    0x00e4: 0x8a,	#  LATIN SMALL LETTER A WITH DIAERESIS
    0x00e5: 0x8c,	#  LATIN SMALL LETTER A WITH RING ABOVE
    0x00e6: 0xbe,	#  LATIN SMALL LETTER AE
    0x00e7: 0x8d,	#  LATIN SMALL LETTER C WITH CEDILLA
    0x00e8: 0x8f,	#  LATIN SMALL LETTER E WITH GRAVE
    0x00e9: 0x8e,	#  LATIN SMALL LETTER E WITH ACUTE
    0x00ea: 0x90,	#  LATIN SMALL LETTER E WITH CIRCUMFLEX
    0x00eb: 0x91,	#  LATIN SMALL LETTER E WITH DIAERESIS
    0x00ec: 0x93,	#  LATIN SMALL LETTER I WITH GRAVE
    0x00ed: 0x92,	#  LATIN SMALL LETTER I WITH ACUTE
    0x00ee: 0x94,	#  LATIN SMALL LETTER I WITH CIRCUMFLEX
    0x00ef: 0x95,	#  LATIN SMALL LETTER I WITH DIAERESIS
    0x00f1: 0x96,	#  LATIN SMALL LETTER N WITH TILDE
    0x00f2: 0x98,	#  LATIN SMALL LETTER O WITH GRAVE
    0x00f3: 0x97,	#  LATIN SMALL LETTER O WITH ACUTE
    0x00f4: 0x99,	#  LATIN SMALL LETTER O WITH CIRCUMFLEX
    0x00f5: 0x9b,	#  LATIN SMALL LETTER O WITH TILDE
    0x00f6: 0x9a,	#  LATIN SMALL LETTER O WITH DIAERESIS
    0x00f7: 0xd6,	#  DIVISION SIGN
    0x00f8: 0xbf,	#  LATIN SMALL LETTER O WITH STROKE
    0x00f9: 0x9d,	#  LATIN SMALL LETTER U WITH GRAVE
    0x00fa: 0x9c,	#  LATIN SMALL LETTER U WITH ACUTE
    0x00fb: 0x9e,	#  LATIN SMALL LETTER U WITH CIRCUMFLEX
    0x00fc: 0x9f,	#  LATIN SMALL LETTER U WITH DIAERESIS
    0x00ff: 0xd8,	#  LATIN SMALL LETTER Y WITH DIAERESIS
    0x0131: 0xf5,	#  LATIN SMALL LETTER DOTLESS I
    0x0152: 0xce,	#  LATIN CAPITAL LIGATURE OE
    0x0153: 0xcf,	#  LATIN SMALL LIGATURE OE
    0x0178: 0xd9,	#  LATIN CAPITAL LETTER Y WITH DIAERESIS
    0x0192: 0xc4,	#  LATIN SMALL LETTER F WITH HOOK
    0x02c6: 0xf6,	#  MODIFIER LETTER CIRCUMFLEX ACCENT
    0x02c7: 0xff,	#  CARON
    0x02d8: 0xf9,	#  BREVE
    0x02d9: 0xfa,	#  DOT ABOVE
    0x02da: 0xfb,	#  RING ABOVE
    0x02db: 0xfe,	#  OGONEK
    0x02dc: 0xf7,	#  SMALL TILDE
    0x02dd: 0xfd,	#  DOUBLE ACUTE ACCENT
    0x03a9: 0xbd,	#  GREEK CAPITAL LETTER OMEGA
    0x03c0: 0xb9,	#  GREEK SMALL LETTER PI
    0x2013: 0xd0,	#  EN DASH
    0x2014: 0xd1,	#  EM DASH
    0x2018: 0xd4,	#  LEFT SINGLE QUOTATION MARK
    0x2019: 0xd5,	#  RIGHT SINGLE QUOTATION MARK
    0x201a: 0xe2,	#  SINGLE LOW-9 QUOTATION MARK
    0x201c: 0xd2,	#  LEFT DOUBLE QUOTATION MARK
    0x201d: 0xd3,	#  RIGHT DOUBLE QUOTATION MARK
    0x201e: 0xe3,	#  DOUBLE LOW-9 QUOTATION MARK
    0x2020: 0xa0,	#  DAGGER
    0x2021: 0xe0,	#  DOUBLE DAGGER
    0x2022: 0xa5,	#  BULLET
    0x2026: 0xc9,	#  HORIZONTAL ELLIPSIS
    0x2030: 0xe4,	#  PER MILLE SIGN
    0x2039: 0xdc,	#  SINGLE LEFT-POINTING ANGLE QUOTATION MARK
    0x203a: 0xdd,	#  SINGLE RIGHT-POINTING ANGLE QUOTATION MARK
    0x2044: 0xda,	#  FRACTION SLASH
    0x20ac: 0xdb,	#  EURO SIGN
    0x2122: 0xaa,	#  TRADE MARK SIGN
    0x2202: 0xb6,	#  PARTIAL DIFFERENTIAL
    0x2206: 0xc6,	#  INCREMENT
    0x220f: 0xb8,	#  N-ARY PRODUCT
    0x2211: 0xb7,	#  N-ARY SUMMATION
    0x221a: 0xc3,	#  SQUARE ROOT
    0x221e: 0xb0,	#  INFINITY
    0x222b: 0xba,	#  INTEGRAL
    0x2248: 0xc5,	#  ALMOST EQUAL TO
    0x2260: 0xad,	#  NOT EQUAL TO
    0x2264: 0xb2,	#  LESS-THAN OR EQUAL TO
    0x2265: 0xb3,	#  GREATER-THAN OR EQUAL TO
    0x25ca: 0xd7,	#  LOZENGE
    0xf8ff: 0xf0,	#  Apple logo
    0xfb01: 0xde,	#  LATIN SMALL LIGATURE FI
    0xfb02: 0xdf,	#  LATIN SMALL LIGATURE FL
}
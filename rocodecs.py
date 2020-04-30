#!/usr/bin/env python
"""
Module to register RISC OS alphabets as encodings with the Python codec system.

The encodings registered here are the alphabets used by RISC OS, based on the standard Python
codecs. The encodings are registered in the following format:

    riscos-alphabet-<alphabet number>
    riscos-<lower case alphabet name as given by UK territory>

This should allow the encodings to be located programatically whichever of those values are
used. The 'riscos-alphabet-111' and 'riscos-utf8' encodings are registered for orthoginality,
and map directly to the 'utf-8' encoding.

The encodings supplied here include characters in the C1 region (0x80-0x9F) to match the
representations within RISC OS. Two characters, 0x84 and 0x87 are not representable.

The 0x84 character is the 'resize' character, which does exist as a character in unicode,
but encodes into surrogates within Python. Because this breaks the single-character mapping
implementation used here, it has been mapped to the replacement character.

The 0x87 character is represented as '87' in the character set and otherwise unmapped
in RISC OS, so has been mapped to the replacement character.

Some character sets, in their specification define that code points must not be used, which
means that they are not defined within the Python codecs. As characters do exist at those
code points within RISC OS, they should be provided with a mapping, but at present are left
with replacement the character.

Importing this module will immediately register the new codecs.

This module is intentionally Python 2/3 compatible as Python 2 code will remain for some
time.
"""

import codecs
import sys


class RISCOSAlphabet(object):
    base_array = bytes(bytearray(range(256)))

    def __init__(self, alphabet, name, base_encoding, changes=None):
        """
        Create an 8bit encoding, based on a known encoding, with some code point changes.

        @param alphabet:        RISC OS Alphabet number
        @param name:            Encoding name to use within Python codecs
        @param base_encoding:   Encoding name to use as the basis for the encoding
        @param changes:         Changes made to the encoding, as a list of dictionaries of
                                code-point -> unicode character pairs.
        """
        self.alphabet = alphabet
        self.name = name
        self.base_encoding = base_encoding
        self.decode_table = list(self.base_array.decode(base_encoding, 'replace'))
        changes = changes or [{}]
        # Apply the changes from the array
        for change in changes:
            for codepoint, value in change.items():
                self.decode_table[codepoint] = value
        self.encode_table = {char: (index) for index, char in enumerate(self.decode_table)}
        self.codec = codecs.CodecInfo(self.encode, self.decode, name=name)
        self.decode_readers = {
                'strict': self._decode_strict,
                'ignore': self._decode_ignore,
                'replace': self._decode_replace,
            }
        self.encode_readers = {
                'strict': self._encode_strict,
                'ignore': self._encode_ignore,
                'replace': self._encode_replace,
            }

    def __repr__(self):
        return "<{}(alphabet={}, name={})>".format(self.__class__.__name__,
                                                   self.alphabet,
                                                   self.name)

    def encode(self, text, errors='replace'):
        encoder = self.encode_readers[errors]
        return (bytes(bytearray(encoder(char) for char in text)), len(text))

    def _encode_strict(self, c):
        nc = self.encode_table.get(c, None)
        if nc is None:
            raise UnicodeEncodeError("Cannot encode character {!r} with encoding '{}'".format(c, self.name))
        return nc

    def _encode_ignore(self, c):
        return self.encode_table.get(c, '')

    def _encode_replace(self, c):
        return self.encode_table.get(c, '?')

    # 'bytes' works differently between python 2 and python 3.
    # In python 2, it's a str, so enumerating it returns individual characters as strings.
    # In python 3, it's a bytes, and enumerating it returns the ordinal value.
    if sys.version_info.major == 2:
        def decode(self, binary, errors='strict'):
            decoder = self.decode_readers[errors]
            return (''.join(decoder(ord(x)) for x in binary), len(binary))
    else:
        def decode(self, binary, errors='strict'):
            decoder = self.decode_readers[errors]
            return (''.join(decoder(x) for x in binary), len(binary))

    def _decode_strict(self, c):
        nc = self.decode_table[c]
        if nc is u'\ufffd':
            raise UnicodeDecodeError("Cannot decode character {!r} from encoding '{}'".format(c, self.name))
        return nc

    def _decode_ignore(self, c):
        nc = self.decode_table[c]
        if nc is u'\ufffd':
            return ''
        return nc

    def _decode_replace(self, c):
        return self.decode_table[c]


class RISCOSUTF8(RISCOSAlphabet):

    def __init__(self, alphabet, name):
        """
        A representation of the UTF-8 on RISC OS, purely so that we map to standard UTF-8 codec.
        """
        self.alphabet = alphabet
        self.name = name
        self.base_encoding = 'utf-8'
        self.codec = codecs.lookup(self.base_encoding)


c1_changes = {
        0x80: u'\u20AC', # euro
        0x81: u'\u0174', # W circumflex
        0x82: u'\u0175', # w circumflex
        0x83: u'\u25F0', # resize icon
        0x84: u'\uFFFD', # close icon: should be u'\U0001FBC0', but that gets encoded into surrogates, which breaks the map
        0x85: u'\u0176', # Y circumflex
        0x86: u'\u0177', # y circumflex
        0x87: u'\uFFFD', # 0x87 cannot be represented in unicode
        0x88: u'\u21E6', # left
        0x89: u'\u21E8', # right
        0x8a: u'\u21E9', # down
        0x8b: u'\u21E7', # up
        0x8c: u'\u2026', # ellipsis
        0x8d: u'\u2122', # TM
        0x8e: u'\u2030', # permille
        0x8f: u'\u2022', # bullet
        0x90: u'\u2018', # left quote
        0x91: u'\u2019', # right quote
        0x92: u'\u2039', # left single guillemet
        0x93: u'\u203A', # right single guillemet
        0x94: u'\u201C', # left double quote
        0x95: u'\u201D', # right double quote
        0x96: u'\u201E', # right double quote as base line
        0x97: u'\u2013', # en dash
        0x98: u'\u2014', # em dash
        0x99: u'\u2212', # minus
        0x9a: u'\u0152', # OE ligature
        0x9b: u'\u0153', # oe ligature
        0x9c: u'\u2020', # dagger
        0x9d: u'\u2021', # double dagger
        0x9e: u'\uFB01', # fi ligature
        0x9f: u'\uFB02', # fl ligature
    }
welsh_changes = {
        0xa8: u'\u1e80', # W grave
        0xaa: u'\u1e82', # W acute
        0xac: u'\u1ef2', # Y grave
        0xaf: u'\u0178', # Y umlaut
        0xb8: u'\u1e81', # w grave
        0xba: u'\u1e83', # w acute
        0xbc: u'\u1ef3', # y grave
        0xbd: u'\u1e84', # W umlaut
        0xbe: u'\u1e85', # w umlaut
        0xd0: u'\u0174', # W circumflex
        0xde: u'\u0176', # Y circumflex
        0xf1: u'\u0175', # w circumflex
        0xfe: u'\u0177', # y circumflex
    }

# Python does not map some characters in its iso-8859-3 mapping.
# Consult https://www.ecma-international.org/publications/files/ECMA-ST/Ecma-094.pdf for the correct mapping.
iso8859_3_changes = {
        0xa5: u'\u00a5', # Yen
        0xae: u'\u00ae', # Registered trade mark
        0xbe: u'\u00be', # 3/4
        0xc3: u'\u00c3', # Latin Capital Letter A with Tilde
        0xd0: u'\u00d0', # Latin Capital Letter Eth
        0xe3: u'\u00e3', # Latin Small Letter A with Tilde
        0xf0: u'\u00f0', # Latin Small Letter Eth
    }

# Note: Many characters are unmapped in ISO 8859-6.
# Consult https://www.ecma-international.org/publications/files/ECMA-ST/Ecma-114.pdf for details.
iso8859_6_changes = {
        # FIXME: This should be filled with the characters as used by RISC OS.
        0xa1: u'\ufffd', # ?
        0xa2: u'\ufffd', # ?
        0xa3: u'\ufffd', # ?
        0xa5: u'\ufffd', # ?
        0xa6: u'\ufffd', # ?
        0xa7: u'\ufffd', # ?
        0xa8: u'\ufffd', # ?
        0xa9: u'\ufffd', # ?
        0xaa: u'\ufffd', # ?
        0xab: u'\ufffd', # ?
        0xae: u'\ufffd', # ?
        0xaf: u'\ufffd', # ?
        0xb0: u'\ufffd', # ?
        0xb1: u'\ufffd', # ?
        0xb2: u'\ufffd', # ?
        0xb3: u'\ufffd', # ?
        0xb4: u'\ufffd', # ?
        0xb5: u'\ufffd', # ?
        0xb6: u'\ufffd', # ?
        0xb7: u'\ufffd', # ?
        0xb8: u'\ufffd', # ?
        0xb9: u'\ufffd', # ?
        0xba: u'\ufffd', # ?
        0xbc: u'\ufffd', # ?
        0xbd: u'\ufffd', # ?
        0xbe: u'\ufffd', # ?
        0xc0: u'\ufffd', # ?
        0xdb: u'\ufffd', # ?
        0xdc: u'\ufffd', # ?
        0xdd: u'\ufffd', # ?
        0xde: u'\ufffd', # ?
        0xdf: u'\ufffd', # ?
        0xf3: u'\ufffd', # ?
        0xf4: u'\ufffd', # ?
        0xf5: u'\ufffd', # ?
        0xf6: u'\ufffd', # ?
        0xf7: u'\ufffd', # ?
        0xf8: u'\ufffd', # ?
        0xf9: u'\ufffd', # ?
        0xfa: u'\ufffd', # ?
        0xfb: u'\ufffd', # ?
        0xfc: u'\ufffd', # ?
        0xfd: u'\ufffd', # ?
        0xfe: u'\ufffd', # ?
        0xff: u'\ufffd', # ?
    }

# Note: 3 characters are unmapped in ISO 8859-7.
# Consult https://www.ecma-international.org/publications/files/ECMA-ST/Ecma-118.pdf for details.
iso8859_7_changes = {
        # FIXME: This should be filled with the characters as used by RISC OS.
        0xaa: u'\ufffd', # ?
        0xae: u'\ufffd', # ?
        0xd2: u'\ufffd', # ?
        0xff: u'\ufffd', # ?
    }

# Note: Many characters are unmapped in ISO 8859-8.
# Consult https://www.ecma-international.org/publications/files/ECMA-ST/Ecma-121.pdf for details.
iso8859_8_changes = {
        # FIXME: This should be filled with the characters as used by RISC OS.
        0xa1: u'\ufffd', # ?
        0xbf: u'\ufffd', # ?
        0xc0: u'\ufffd', # ?
        0xc1: u'\ufffd', # ?
        0xc2: u'\ufffd', # ?
        0xc3: u'\ufffd', # ?
        0xc4: u'\ufffd', # ?
        0xc5: u'\ufffd', # ?
        0xc6: u'\ufffd', # ?
        0xc7: u'\ufffd', # ?
        0xc8: u'\ufffd', # ?
        0xc9: u'\ufffd', # ?
        0xca: u'\ufffd', # ?
        0xcb: u'\ufffd', # ?
        0xcc: u'\ufffd', # ?
        0xcd: u'\ufffd', # ?
        0xce: u'\ufffd', # ?
        0xcf: u'\ufffd', # ?
        0xd0: u'\ufffd', # ?
        0xd1: u'\ufffd', # ?
        0xd2: u'\ufffd', # ?
        0xd3: u'\ufffd', # ?
        0xd4: u'\ufffd', # ?
        0xd5: u'\ufffd', # ?
        0xd6: u'\ufffd', # ?
        0xd7: u'\ufffd', # ?
        0xd8: u'\ufffd', # ?
        0xd9: u'\ufffd', # ?
        0xda: u'\ufffd', # ?
        0xdb: u'\ufffd', # ?
        0xdc: u'\ufffd', # ?
        0xdd: u'\ufffd', # ?
        0xde: u'\ufffd', # ?
        0xfb: u'\ufffd', # ?
        0xfc: u'\ufffd', # ?
        0xff: u'\ufffd', # ?
    }

riscos_alphabets = [
        # 100 is BBCFont
        RISCOSAlphabet(101, 'riscos-latin1', 'iso-8859-1', changes=[c1_changes]),
        RISCOSAlphabet(102, 'riscos-latin2', 'iso-8859-2', changes=[c1_changes]),
        RISCOSAlphabet(103, 'riscos-latin3', 'iso-8859-3', changes=[c1_changes, iso8859_3_changes]),
        RISCOSAlphabet(104, 'riscos-latin4', 'iso-8859-4', changes=[c1_changes]),
        RISCOSAlphabet(105, 'riscos-cyrillic', 'iso-8859-5', changes=[c1_changes]),
        RISCOSAlphabet(106, 'riscos-arabic', 'iso-8859-6', changes=[c1_changes, iso8859_6_changes]),
        RISCOSAlphabet(107, 'riscos-greek', 'iso-8859-7', changes=[c1_changes, iso8859_7_changes]),
        RISCOSAlphabet(108, 'riscos-hebrew', 'iso-8859-8', changes=[c1_changes, iso8859_8_changes]),
        RISCOSAlphabet(109, 'riscos-latin5', 'iso-8859-9', changes=[c1_changes]),
        RISCOSAlphabet(110, 'riscos-welsh', 'iso-8859-1', changes=[c1_changes, welsh_changes]),  # ISO-IR-182
        RISCOSUTF8(111, 'riscos-utf8'), # The lack of hyphen matches convention for alphabet names
        RISCOSAlphabet(112, 'riscos-latin9', 'iso-8859-15', changes=[c1_changes]),
        RISCOSAlphabet(113, 'riscos-latin6', 'iso-8859-10', changes=[c1_changes]),
        RISCOSAlphabet(114, 'riscos-latin7', 'iso-8859-13', changes=[c1_changes]),
        RISCOSAlphabet(115, 'riscos-latin8', 'iso-8859-14', changes=[c1_changes]),
        RISCOSAlphabet(116, 'riscos-latin10', 'iso-8859-16', changes=[c1_changes]),
    ]
riscos_alphabets_map = {encoding.name: encoding.codec for encoding in riscos_alphabets}
def custom_search_function(encoding_name):
    if encoding_name.startswith('riscos-alphabet-'):
        _, _, number = encoding_name.split('-', 2)
        try:
            alphabet_number = int(number)
            for encoding in riscos_alphabets:
                if encoding.alphabet == alphabet_number:
                    return encoding.codec
        except ValueError:
            return None
    return riscos_alphabets_map.get(encoding_name, None)


codecs.register(custom_search_function)

# Python codecs for RISC OS alphabets

This repository contains an implementation of codecs mapping the RISC OS alphabets to Unicode
and vice-versa. The RISC OS alphabets mostly follow the standards, but diverge in the C1
region and where the standards do not define characters.

## Codecs

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

# Usage

Importing this module will immediately register the new codecs.

# Compatibility

This module is intentionally Python 2/3 compatible as Python 2 code will remain for some
time.

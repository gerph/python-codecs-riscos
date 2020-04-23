#!/usr/bin/env python
"""
Check which characters are not mapped.
"""

import rocodecs

# Display where the encodings are not covered.
for encoding in rocodecs.riscos_alphabets:
    print("Checking encoding {}".format(encoding.name))
    if encoding.name == 'riscos-utf8':
        print("  Skipping")
        continue

    encoded = rocodecs.RISCOSAlphabet.base_array.decode(encoding.name)
    for index in range(0x20, 0x100):
        if encoded[index] == u'\ufffd':
            print("  &{:02x}: No unicode character mapping".format(index))

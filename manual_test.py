#!/usr/bin/env python
"""
Really not-extensive test of the codecs.
"""

import rocodecs


def main():
    binary = b'abcdefg\x80\xa5\xb8'

    # Decode
    text = binary.decode('riscos-latin3', 'replace')
    print(repr(text))

    # Encode
    binary2 = text.encode('riscos-latin1')
    print(repr(binary2))

    assert binary == binary2


if __name__ == '__main__':
    main()

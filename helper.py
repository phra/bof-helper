#!/usr/bin/env python

import sys
import struct
import socket

DEBUG = True

def u8(x):
    return struct.unpack("<B", x)[0]

def u16(x):
    return struct.unpack("<H", x)[0]

def u32(x):
    return struct.unpack("<I", x)[0]

def u64(x):
    return struct.unpack("<Q", x)[0]

def p8(x):
    return struct.pack("<B", x)

def p16(x):
    return struct.pack("<H", x)

def p32(x):
    return struct.pack("<I", x)

def p64(x):
    return struct.pack("<Q", x)

def log(x):
    print(x)

def debug(x):
    log("[*] {:s}".format(x)) if DEBUG else None

def ok(x):
    log("[+] {:s}".format(x))

def err(x):
    log("[-] {:s}".format(x))

def warn(x):
    log("[!] {:s}".format(x))

def pattern_create(length = 8192, unicode = False):
    pattern = ''
    parts = ['A', 'a', '0'] if not unicode else ['A\x00', 'a\x00', '0\x00']
    try:
        if not isinstance(length, (int, long)) and length.startswith('0x'):
            length = int(length, 16)
        elif not isinstance(length, (int, long)):
            length = int(length, 10)
    except ValueError:
        print 'ValueError'
        sys.exit(254)
    while len(pattern) != (length * (2 if unicode else 1)):
        pattern += parts[(len(pattern) / (2 if unicode else 1)) % 3]
        if len(pattern) % 3 == 0:
            parts[2] = chr(ord(parts[2][:1]) + 1) + ('\x00' if unicode else '')
            if parts[2][:1] > '9':
                parts[2] = '0' + ('\x00' if unicode else '')
                parts[1] = chr(ord(parts[1][:1]) + 1) + ('\x00' if unicode else '')
                if parts[1][:1] > 'z':
                    parts[1] = 'a' + ('\x00' if unicode else '')
                    parts[0] = chr(ord(parts[0][:1]) + 1) + ('\x00' if unicode else '')
                    if parts[0][:1] > 'Z':
                        parts[0] = 'A' + ('\x00' if unicode else '')
    return pattern

def pattern_offset(value, length = 8192):
    original_value = value
    try:
        if value.startswith('0x'):
            value = struct.pack('<I', int(value, 16))
    except ValueError:
        raise Exception('pattern_offset: invalid value ' + value)
    pattern = pattern_create(length)
    try:
        return pattern.index(value)
    except ValueError:
        try:
            index = pattern_create(length, True).index(value)
            warn("Unicode pattern matching")
            return index
        except ValueError:
            raise Exception('pattern_offset: ' + original_value + ' not found')

def generate_badchars(avoid = ''):
    badchars = ''
    badchars_print = ''
    for i in range(0x20, 255):
        if not chr(i) in avoid:
            badchars += chr(i)
            badchars_print += '\\x' + hex(i)[2:].rjust(2, '0')
    print "generated badchars:"
    print badchars_print
    return badchars

def save_file(filename, content):
    print 'generating %s.. [size: %d]' % (filename, len(content))
    f = open(filename, 'w')
    f.write(content)
    f.close()

def fill(payload, total_length, filler = 'D'):
    if (total_length - len(payload)) >= 0:
        return 'D' * (total_length - len(payload))
    else:
        raise Exception('payload too big')

def connect_tcp(host, port):
    print("[TCP] connected to %s:%d" %(host, port))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    return s

def connect_udp():
    print("[UDP] create UDP socket")
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return s

def print_help():
    print 'Usage: %s create <buflen>' % sys.argv[0]
    print 'Usage: %s offset <value> [buflen=8192]' % sys.argv[0]
    sys.exit(-1)

def main():
    if len(sys.argv) < 3 or sys.argv[1].lower() not in ['create', 'offset']:
        print_help()

    command = sys.argv[1].lower()
    num_value = sys.argv[2]

    if command == 'create':
        print pattern_create(num_value)
    elif len(sys.argv) == 4:
        print pattern_offset(num_value, sys.argv[3])
    else:
        print pattern_offset(num_value)

if __name__ == '__main__':
    main()

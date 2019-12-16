# bof-helper
Python Helper Utilities for SEH Overwrite Based Exploits

## Usage
```py
from helper import *
```

## Examples

1. pattern

```py
payload = pattern_create(3000)
```

2. offset

```py
nSEH_offset = pattern_offset('0x39644338')
egghunter_offset = pattern_offset('3Av4')
```

3. padding

```py
payload = pattern_create(egghunter_offset)
payload += egghunter
payload += fill(payload, farjmp_offset)
payload += farjmp
payload += fill(payload, nSEH_offset)
```

4. save_file

```py
save_file("payload.txt", payload)
```

5. packing

```py
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
```

6. logging

```py
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
```

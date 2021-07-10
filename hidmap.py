KEYCODEMAP = {}

for code in range(26):
    KEYCODEMAP[chr(0x61 + code)] = (0, 4 + code)
    KEYCODEMAP[chr(0x41 + code)] = (2, 4 + code)

NUM_SPCHAR ="!@#$%^&*()"

for code in range(1, 11):
    KEYCODEMAP[chr(0x30+(code%10))] = (0, 0x1d + code)
    KEYCODEMAP[NUM_SPCHAR[code -1]] = (2, 0x1d + code)

KEYCODEMAP['\n'] = (0, 0x28)
KEYCODEMAP['\b'] = (0, 0x2a)
KEYCODEMAP['\t'] = (0, 0x2b)
KEYCODEMAP[' '] = (0, 0x2c)
KEYCODEMAP['-'] = (0, 0x2d)
KEYCODEMAP['_'] = (2, 0x2d)
KEYCODEMAP['='] = (0, 0x2e)
KEYCODEMAP['+'] = (2, 0x2e)
KEYCODEMAP['['] = (0, 0x2f)
KEYCODEMAP['{'] = (2, 0x2f)
KEYCODEMAP[']'] = (0, 0x30)
KEYCODEMAP['}'] = (2, 0x30)
KEYCODEMAP['\\'] = (0, 0x31)
KEYCODEMAP['|'] = (2, 0x31)
KEYCODEMAP[';'] = (0, 0x33)
KEYCODEMAP[':'] = (2, 0x33)
KEYCODEMAP['\''] = (0, 0x34)
KEYCODEMAP['"'] = (2, 0x34)
KEYCODEMAP[','] = (0, 0x36)
KEYCODEMAP['<'] = (2, 0x36)
KEYCODEMAP['.'] = (0, 0x37)
KEYCODEMAP['>'] = (2, 0x37)
KEYCODEMAP['/'] = (0, 0x38)
KEYCODEMAP['?'] = (2, 0x38)


ALTKEYPADMAP = {}

for i in range(1,11):
    ALTKEYPADMAP[chr(0x30+(i % 10))] = (0x04, 0x58+i)

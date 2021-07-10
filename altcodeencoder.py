from hidmap import KEYCODEMAP, ALTKEYPADMAP


def altcodeencoder(s, codepage):
    ret = []
    lastchar = None
    for c in s:
        encoded = c.encode(codepage)
        if ord(c) < 128:
            if lastchar == c:
                ret.append((0,0))
            ret.append(KEYCODEMAP[c])
            lastchar = c
        else: # Windows codepage
            n = int.from_bytes(encoded, 'big')
            if n < 256:
                ret.append((0x04, ALTKEYPADMAP['0'][1]))
            for c in str(n):
                if lastchar == c:
                    ret.append((0x04,0))
                ret.append((0x04, ALTKEYPADMAP[c][1]))
                lastchar = c
            ret.append((0,0))
    ret.append((0,0))
    return ret


def encoder(codes):
    ret = ['#!/bin/sh']
    for i in codes:
        ret.append(f'echo -ne "\\x{i[0]:02x}\\0\\x{i[1]:02x}\\0\\0\\0\\0\\0" > /dev/hidg0')
    return '\n'.join(ret)

# TEST ©®™•§†‡

with open('altcodeencoder.py') as f:
    with open('altcode_inject.sh', 'w') as g:
        g.write(encoder(altcodeencoder(f.read(), 'cp1252')))

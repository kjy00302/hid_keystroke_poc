from hidmap import KEYCODEMAP, ALTKEYPADMAP


def chartoseq(c, cp):
    ret = []
    encoded = c.encode(cp)
    if ord(c) < 128: # Ascii
        ret.append(KEYCODEMAP[c])
        return False, ret
    else: # Windows codepage
        n = int.from_bytes(encoded, 'big')
        if n < 256:
            ret.append((0x04, ALTKEYPADMAP['0'][1]))
        for c in str(n):
            ret.append((0x04, ALTKEYPADMAP[c][1]))
        ret.append((0x00, 0x00))
        return True, ret

def listfill(a):
    for _ in range(8 - len(a)):
        a.append(0)

def altcodeencoder(s, codepage):
    ret = []
    hidcmd = None
    #privisaltcode = False
    state = None
    dupcheckpool = []
    chars = []

    for c in s:
        isalt, seq = chartoseq(c, codepage)
        #if privisaltcode: # TODO Optimize key release
            #ret.append(([0,0,0,0,0,0,0,0], 'release from altcode'))
        #privisaltcode = isalt
        for cmd in seq:
            if state == None:
                state = cmd[0]
                hidcmd = [state, 0]
            if cmd[1] in dupcheckpool:
                # when key duplicates -> flush, release
                dupcheckpool.clear()
                listfill(hidcmd)
                ret.append((hidcmd.copy(), f'dup: flush ({"".join(chars)})'))
                chars.clear()
                hidcmd = [state, 0]
                ret.append(([0,0,0,0,0,0,0,0], 'dup: release'))
                #privisaltcode = False
            if state != cmd[0]:
                # when modifier changes -> flush
                listfill(hidcmd)
                ret.append((hidcmd.copy(), f'mod: flush ({"".join(chars)})'))
                chars.clear()
                state = cmd[0]
                hidcmd = [state, 0]
            if len(hidcmd) == 8:
                # when command is full -> flush
                ret.append((hidcmd.copy(), f'len: flush ({"".join(chars)})'))
                chars.clear()
                hidcmd = [state, 0]
            hidcmd.append(cmd[1])
            dupcheckpool.append(cmd[1])
            if c != '\n':
                chars.append(c)
    listfill(hidcmd)
    ret.append((hidcmd.copy(), 'terminate'))
    ret.append(([0,0,0,0,0,0,0,0], 'release'))
    return ret


def encoder(codes):
    cnt = 0
    ret = ['#!/bin/sh']
    for i, comment in codes:
        cnt += 1
        ret.append(f'echo -ne "\\x{i[0]:02x}\\0\\x{i[2]:02x}\\x{i[3]:02x}\\x{i[4]:02x}\\x{i[5]:02x}\\x{i[6]:02x}\\x{i[7]:02x}" > /dev/hidg0 # {comment}')
        if cnt == 2048:
            #ret.append('sleep 0.5') # TODO find optimal delay
            cnt = 0
    return '\n'.join(ret)

with open('chordingencoder.py') as f:
    with open('chord_inject.sh', 'w') as g:
        g.write(encoder(altcodeencoder(f.read(), 'cp1252')))

import numpy as np


def str2vec(_str):
    """ vectorize the captcha str """
    vec = np.zeros(4 * 61)
    for i, ch in enumerate(_str):
        offset = i*61 + (ord(ch)-ord('0'))
        vec[offset] = 1
    # print vec
    return vec


def vec2str(vec):
    """ transform the vector to captcha str"""
    _str = ""
    for i in range(4):
        v = vec[i*61: (i+1)*61]
        _str += str(chr(np.argwhere(v == 1)[0][0]+ord('0')))
        # _str += str(np.argwhere(v == 1)[0][0])
    return _str


# print vec2str(str2vec("0819"))

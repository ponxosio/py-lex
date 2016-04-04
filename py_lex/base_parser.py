from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import (ascii, bytes, chr, dict, filter, hex, input,
                      int, map, next, oct, open, pow, range, round,
                      str, super, zip)

class BaseParser(object):

    '''
    Identity length always returns 0
    len(self)
    -> int
    '''
    def __len__(self):
        return 0

    '''
    Identity getter returns word given to it
    self[key]
    key: str -> Set[str]
    '''
    def __getitem__(self, key):
        return set([key])

    '''
    Identity getter returns word given to it
    key: str -> Set[str]
    '''
    def get_refs(self, key):
        return set([key])

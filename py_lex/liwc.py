# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import (ascii, bytes, chr, dict, filter, hex, input,
                      int, map, next, oct, open, pow, range, round,
                      str, super, zip)

import re
import json
from collections import Counter
from itertools import tee

class Liwc(object):

    def __init__(self, liwc_filepath):

        if liwc_filepath:
            self.load_and_parse(liwc_filepath)


    '''
    Reads the LIWC file format:

        %
        1   funct
        2   pronoun
        %
        a   1   10
        abdomen*    146 147
        about   1   16  17

    Returns a tuple of
        * categories Set(categories) from dict(String: Int)
        * stems dict(String: Set(categories))
        * stems_to_categories dict(Stem: Set())
    '''

    def read_token(self, token):
        categories = set()
        prefixes = self.stem_search_trie.prefixes(token)

        if token in self.stem_lookup:
            categories.add(self.stem_int_dict[token])

        if prefixes is not None:
            for prefix in prefixes:
                categories.add(self.stem_int_dict[prefix])

        return categories


    def load(self, pickle_filepath):
        pass

    def dump(self, pickle_filepath):
        pass

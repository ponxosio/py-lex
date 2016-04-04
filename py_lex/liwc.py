# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import (ascii, bytes, chr, dict, filter, hex, input,
                      int, map, next, oct, open, pow, range, round,
                      str, super, zip)

import re
import json
import pickle

from collections import Counter
from itertools import chain

from py_lex.base import Base
from py_lex.liwc_parser import LiwcParser

class Liwc(Base):

    def __init__(self, liwc_filepath=None):

        if liwc_filepath:
            with open(liwc_filepath) as liwc_file:
                self.parser = self.load_and_parse(liwc_file)

    '''
    Reads the LIWC file format:

        %
        1   funct
        2   pronoun
        %
        a   1   10
        abdomen*    146 147
        about   1   16  17

    Returns a parser object that can tell the LIWC categories of a
    given word efficiently.
    '''
    def load_and_parse(self, liwc_file):
        return LiwcParser(liwc_file.read().splitlines())

    '''
    Inherited from base

    token: str -> Set(str)
    '''
    # def categorize_token(self, token):

    '''
    Inherited from base

    For each word string return a tuple (str, Set()) in place.

    This is far less efficient than just counting them.
    [
        ['a', 'tokenized', 'sentence', '.'],
        ['within', 'a', 'single', 'document', '.'],
        ...
    ]
    ->
    [
        [('A', Set('pronoun')), ...],
        ...
    ]
    doc: List[List[str]], ignore_sentences: Bool || True ->
        List[List[(str, Set(str))]]
    '''
    # def annotate_doc(self, doc, ignore_sentences=False):

    # def summarize_doc(self, doc):

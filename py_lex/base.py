# -*- coding: utf-8 -*-
'''
Abstract class that implements shared logic and shows the complete API
'''
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

from py_lex.base_parser import BaseParser

class Base(object):

    def __init__(self):
        self.parser = BaseParser()

    '''
    token: str -> Set(str)
    '''
    def categorize_token(self, token):
        return self.parser[token]

    def categorize_doc(self, doc, ignore_sentences=True):
        if ignore_sentences:
            return [ self.categorize_token(word.lower()) for word in doc ]
        else:
            return [ [ self.categorize_token(word.lower()) for word in sent ]
                    for sent in doc ]

    '''
    doc: List[List[str]], ignore_sentences: Bool || True ->
        List[List[(str, Set(str))]]
    '''
    def annotate_doc(self, doc, ignore_sentences=True):
        if ignore_sentences:
            return list(zip(doc, self.categorize_doc(doc, True)))
        else:
            return [tuple(zip(tokens, classes)) for (tokens, classes)
                    in zip(doc, self.categorize_doc(doc, False))]

    '''
    doc: List[List[str]], ignore_sentences: Bool || True ->
        Counter(key, int)
    '''
    def summarize_doc(self, doc):
        categorized_doc = self.categorize_doc(doc, ignore_sentences)

        # Strip punctuation for word counts
        wc = len([w for w in doc if re.match('\w+', w)])

        sixltr = sum(len(token) > 6 for token in tokens)

        ctr = Counter(list(self._flatten_list_of_sets(categorized_doc)))
        ctr['sixltr'] = sixltr

        # convert to percentile dict
        percent_dict = {k: v/wc for (k,v) in dict(ctr).items()}
        percent_dict['wc'] = wc
        percent_dict['analytic'] = self.analytic_thinking_score(percent_dict)
        percent_dict['tone'] = self.emotional_tone_score(percent_dict)
        percent_dict['authentic'] = self.authenticity_score(percent_dict)
        return percent_dict

    def load(self, pickle_filepath):
        with open(pickle_filepath, 'rb') as pickle_file:
            self.parser = pickle.load(pickle_file)

    def dump(self, pickle_filepath):
        with open(pickle_filepath, 'wb') as pickle_file:
            pickle.dump(self.parser, pickle_file)

    '''
    l_of_s: List[Set[str]] -> generator List[str]
    '''
    def _flatten_list_of_sets(self, l_of_s):
        return chain.from_iterable([ list(categories)
            for categories in l_of_s ])

    '''
    l_of_s: List[List[Set[str]]] -> generator List[str]
    '''
    def _flatten_list_of_list_of_sets(self, l_of_l_of_s):
        return chain.from_iterable(
                    self._flatten_list_of_sets(l_of_l_of_s))


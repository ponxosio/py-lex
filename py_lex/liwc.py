# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import (ascii, bytes, chr, dict, filter, hex, input,
                      int, map, next, oct, open, pow, range, round,
                      str, super, zip)

import re
import json
import pickle

from collections import Counter, defaultdict
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

    def summarize_doc(self, doc, ignore_sentences=True):
        categorized_doc = self.categorize_doc(doc, ignore_sentences)

        return Counter(list(self._flatten_list_of_sets(categorized_doc)))

    '''
    Where percentile_dict is a dict of percentiles of word per document

    Equivalent to LIWC2015 Analytic Thinking category, previously referred to
    as the Category Dimension Index from:

    Pennebaker J. W., Chung C. K. , Frazee J. , Lavergne G. M.,
    and Beaver D. I. (2014). When small words foretell academic success:
    The case of college admissions essays.
    PLoS ONE 9(12): e115844. doi: 10.1371/journal.pone.0115844.
    '''
    def analytic_thinking_score(percentile_dict):
        c = defaultdict(lambda: 0, percentile_dict)
        return 0.3 + c['article'] + c['preps'] - c['ppron'] - c['ipron'] \
            - c['auxverb'] - c['conj'] - c['adverb'] - c['negate']

    '''
    Where percentile_dict is a dict of percentiles of word per document

    Roughly equivalent to LIWC2015 Emotional Tone category, see:

    Cohn, M.A., Mehl, M.R., & Pennebaker, J.W. (2004).
    Linguistic Markers of Psychological Change Surrounding
    September 11, 2001. Psychological Science, 15, 687-693.
    '''
    def emotional_tone_score(percentile_dict):
        c = defaultdict(lambda: 0, percentile_dict)
        # Social + Emotional Positivity + CogMech + Psychological Distance
        return (c['we'] + c['social']) + \
               (c['posemo'] - c['negemo']) + \
               c['cogmech'] + \
               c['articles'] + c['sixltr'] + \
               -0.05 * c['present'] + -0.05 * c['i']

    '''
    Where percentile_dict is a dict of percentiles of word per document

    Equivalent to LIWC2015 Authenticity category, see Table 4 in:

    Newman, M.L., Pennebaker, J.W., Berry, D.S., & Richards, J.M. (2003).
    Lying words: Predicting deception from linguistic styles.
    Personality and Social Psychology Bulletin, 29, 665-675.
    '''
    def authenticity_score(c):
        c = defaultdict(lambda: 0, percentile_dict)
        return 0.36 * (c['i'] + c['we']) + \
               0.16 * (c['shehe'] + c['they']) + \
               -0.15 * c['negemo'] + \
               0.54 + c['excl'] + \
               -0.2 + c['motion'] 

    '''
    Could not determine formula for clout from cited paper:

    Kacewicz, W., Pennebaker, J.W., Davis, M., Jeon, M., & Graesser, A.C.
    (2013). Pronoun use reflects standings in social hierarchies.
    Journal of Language and Social Psychology.
    Online version 19 September 2013, DOI: 10.1177/0261927X1350265.
    '''
    # def clout_score(percentile_dict):
    #     c = defaultdict(lambda: 0, percentile_dict)
    #     return c['i'] * -0.85 + c['we'] * 0.49 + c['shehe'] * 0.29


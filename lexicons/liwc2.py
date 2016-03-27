# -*- coding: utf-8 -*-
import re
from lexicons.base import Lexicon
from collections import Counter
from itertools import tee
import json

'''
'''

class Liwc2():

    def __init__(self, liwc_filepath):
        self.categories = None
        self.stems = None
        self.stems_to_categories = None

        if liwc_filepath:
            self.load_and_parse(liwc_filepath)

    def _get_category_indices(self, liwc_lines):
        divider_start, divider_stop = \
            tuple(i for i, char in enumerate(liwc_lines) if char is '%') 
        return divider_start + 1, divider_stop

    def _get_category_and_stem_lines(self, liwc_lines):
        cat_start, cat_end = self._get_category_indices(liwc_lines)
        categories = [l.split('\t') for l in liwc_lines[cat_start:cat_end]]
        stems = [l.split('\t') for l in liwc_lines[cat_end+1:]]
        return (categories, stems)

    '''
    [['1', 'funct'], ...] -> {'1': 'funct', ...}
    '''
    def _build_category_int_dict(self, category_lines):
        return { cat[0]:cat[1] for cat in category_lines }

    '''
    [['stem', '1', '3', ...], ...] ->
    { 'stem': set(['1', '3', ...]), ...}
    '''
    def _build_stem_int_dict(self, stem_lines):
        return { stem[0]: set(stem[1:]) for stem in stem_lines }

    '''
    [['stem*', ...], ['stem', ...] ...] ->
    { 'stem*': r'^stem.*', 'stem': r'^stem$', ...}
    '''
    def _build_stem_regex_dict(self, stem_lines):
        def to_regex(stem):
            if stem.endswith('*'):
                return re.compile(r'^' + re.escape(stem[:-1]) + '.*')
            else:
                return re.compile(r'^' + re.escape(stem) + '$')

        return { stem[0]: to_regex(stem[0]) for stem in stem_lines }

    def _build_stem_key_lists(self, stem_lines):
        stems, keys = [], []
        endswith_star = lambda s: str.endswith(s, '*')
        
        for stem in stem_lines:
            (stems if endswith_star(stem[0]) else keys) \
                .append(stem[0].rstrip('*'))

        return stems, set(keys)

    def load_and_parse(self, liwc_filepath):
        with open(liwc_filepath) as liwc_file:
           self.parse(liwc_file.read().splitlines())

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
    def parse(self, liwc_lines):
        print liwc_lines[:70]
        start, end = self._get_category_indices(liwc_lines)
        categories, stems = self._get_category_and_stem_lines(liwc_lines)

        # self.categories = self._build_category_int_dict(categories)
        # print self._build_category_int_dict(categories)
        # self.stem_int_dict = self._build_stem_int_dict(stems)
        # self.stem_regex_dict = self._build_stem_regex_dict(stems)
        stem_search, stem_lookup = self._build_stem_key_lists(stems)
        # print len(stem_search), len(stem_lookup)

    '''
    So that given a token:
    1. Identify matching LIWC stems
    2. Lookup stems categories
    yields Set of categories
    '''
    def read_token(self, token):
        categories = set()
        prefixes = self.stem_search_trie.prefixes(token)

        if token in self.stem_lookup:
            categories.add(self.stem_int_dict[token])

        if prefixes is not None:
            for prefix in prefixes:
                categories.add(self.stem_int_dict[prefix])

        yield categories


    def load(self, pickle_filepath):
        pass

    def dump(self, pickle_filepath):
        pass

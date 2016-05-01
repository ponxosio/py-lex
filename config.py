'''
Preloads the module for an ipython session

PYTHONSTARTUP='./config.py' ipython
'''

import nltk
import py_lex
from py_lex import Liwc, LiwcParser

liwc = Liwc('./lexicons/liwc.dic')

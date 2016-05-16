# `py-lex`

Python library for parsing and applying emotion, socio-psycho, and sentiment datasets to your own text corpora.


## Features

Analyzes at the unigram token of tokenized documents.

Supports datasets of the form of LIWC 2007 dictinoary and NRC EmoLex. This library itself doesn't include any of these datasets you must procure or create them on your own.

* The LIWC 2007 dictionary can be purchased from [their website](http://liwc.wpengine.com/). Other documents that follow the LIWC file format will also work.
* The NRC EmoLex lexicon can be downloaded for free for research purposes from [their website](http://saifmohammad.com/WebPages/NRC-Emotion-Lexicon.htm).

Legal note: using the actual LIWC dataset outside of the application may be a violation of their terms of service. NRC datasets are free to use for research purposes, but require permission for commercial uses.


## Install

Either intall using `pip`:
```
pip install py_lex
```

Or clone and install the requirements (`marisa-trie` and `bidict`), with `pip` this means simply running the following command in the project directory:

```
pip install -r ./requirements.txt
```


## Usage

```Python
from py_lex import Liwc, EmoLex
# A tokenizer of some kind, for example NLTK:
import nltk

# Instantiate reader from raw, local .dic file
lexicon = Liwc('./liwc.dic')
# Or use an NRC EmoLex lexicon, which implements the same API
# lexicon = EmoLex('./emo-lex.txt')

# Or from a previously dumped file for slightly faster instantiation (no parsing)
lexicon.dump('./lexicon.pickle')
lexiconP = Liwc()
lexiconP.load('./lexicon.pickle')

# tokenize your document of choice
document = nltk.tokenize.casual.casual_tokenize(a_str_document)
# => List[str]

summary = lexicon.summarize_doc(document)
# => Dict[str, Union[int, float]]
# Where str is the LIWC/EmoLex key

annotation = lexicon.annotate_doc(document)
# => List[Set[str]]
# Where each index aligns with the input List of words and str is the
# LIWC/EmoLex key for easy zipping.

# faster if you need both, since summarize_doc creates an annotation internally
summary = lexicon.summarize_annotation(annotation)
# => Dict[str, Union[int, float]]
# Where str is the LIWC/EmoLex key

# Get the set of keys being used by the given lexicon
lexicon.keys()
# => Set[str]

# Get the number of keys that the given lexicon will compute
len(lexicon)
# => int # 82
```

# `py-lex`

Python libraries for parsing and applying emotion, socio-psycho, and sentiment datasets to your own text corpora.

## Features

Analyzes at the unigram token of tokenized documents.

Supports datasets of the form of LIWC, NRC EmoLex, and NRC SentiLex. This library itself doesn't include any of these datasets you must procure or create them on your own.

Legal note: using the actual LIWC dataset outside of the application may be a violation of their terms of service. NRC datasets are free to use for research purposes, but require permission for commercial uses.

## Requirements

Py-Lex has two dependencies `marisa-trie` and `bidict`, to install them simply run:

```
pip install -r ./requirements.txt
```

## Usage

```Python
import Liwc from lex

# Instantiate reader from raw, local .dic file
liwc = Liwc('./liwc.dic')

# Or from a previously dumped file for faster instantiation (no parsing)
liwc.dump('./liwc.pickle')
liwcP = Liwc()
liwcP.load('./liwc.pickle')

# tokenize your document of choice
document = nltk.tokenize.casual.casual_tokenize(a_str_document)

summary = liwc.summarize_doc(document)
annotation = liwc.annotate_doc(document)

# faster if you need both, since summary creates an annotation
# returns (annotation, summary) tuple
(annotation, summary) = liwc.summarize_annotation(annotation)
```

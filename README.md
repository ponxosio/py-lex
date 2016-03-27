# `py-lex`

Python libraries for parsing and applying emotion, socio-psycho, and sentiment datasets to your own text corpora.

## Features

Analyzes at the unigram token and document level.

Supports datasets of the form of LIWC, NRC EmoLex, and NRC SentiLex. This library itself doesn't include any of these datasets you must procure or create them on your own.

Legal note: using the actual LIWC dataset outside of the application may be a violation of their terms of service. NRC datasets are free to use for research purposes, but require permission for commercial uses.

## Usage

```Python
import Liwc from lex

# Instantiate reader from raw, local .dic file
liwc = Liwc('./liwc.dic')

# Or from a previously dumped file for faster instantiation (no parsing)
liwc.dump('./liwc.pickle')
liwcP = Liwc()
liwcP.load('./liwc.pickle')

# Or manually parse the LIWC data
liwc.load_and_parse('./liwc.dic')

summary = liwc.summarizeDoc('some document to get a summary')
annotation = liwc.annotateDoc('some document to get a detailed annotation')
summary_of_annotation = liwc.summarizeAnnotation(annotation)
```

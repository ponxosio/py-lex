# Setup

Python and Javascript libraries packaged together here;
mostly they are translations of each other, if both exist (as with LIWC, for example).

## LIWC

- liwc.py and liwc.js require `/usr/local/data/liwc_2007.trie`
  - MD5: bca2eeec79701ed88c40f8c9c75e5f7c
- liwc-regex.js requires `/usr/local/data/liwc_2007.csv`
  - MD5: 686df57d28941cf797704bd2d4f9a1a3

You can get the LIWC lexicon at [liwc.net](http://liwc.net/).

You can use dic2trie to convert the `.dic` file that the LIWC lexicon comes
with to a trie, for faster (streaming) analysis.

## Arabsenti

- arabsenti.py requires `/usr/local/data/arabsenti_lexicon.txt`
  - MD5: 0ed1192e4b6f10a29b353b3056ec179d

You can get the Arabsenti lexicon from [Muhammad Abdul-Mageed](http://mumageed.blogspot.com/).

Citation form:

    @inproceedings{abdul:2011,
      title={Subjectivity and sentiment analysis of modern standard Arabic},
      author={Abdul-Mageed, M. and Diab, M.T. and Korayem, M.},
      booktitle={Proceedings of the 49th Annual Meeting of the Association for
      Computational Linguistics: Human Language Technologies: short papers-Volume 2},
      pages={587--591},
      year={2011},
      organization={Association for Computational Linguistics}
    }

It requires Python 2.7+.

## AFINN

This is publicly available at [Finn Årup Nielsen's blog](http://fnielsen.posterous.com/afinn-a-new-word-list-for-sentiment-analysis), so I just left it in the code.

# Installation

    python setup.py install
    npm install
    npm link

## Scala

Add the following to your `build.sbt`:

    resolvers ++= Seq("repo.codahale.com" at "http://repo.codahale.com")
    libraryDependencies ++= Seq("com.codahale" % "jerkson_2.9.1" % "0.5.0")

Pull the `scala/lexicons.scala` file into your codebase, and run something like:

    val document = "Pierre Venken is my hero, every day I draw inspiration ..."
    val tokens = document.toLowerCase.replaceAll("\\W", " ").split("\\s+")
    val counts = com.henrian.Liwc(tokens)
    val normalized_counts = counts.mapValues(_ / counts("WC"))

## Patching LIWC2007_English100131.dic

For the purpose of using `dict2trie.py`, LIWC may ship with a broken English dictionary.  The MD5 of the broken dictionary is `1d964b7fbf218effd6aa652303e15e9e`. One solution is to patch the dictionary before converting to a trie.  The process might look something like this:

  cp /Applications/LIWC2007/Dictionaries/LIWC2007_English100131.dic /usr/local/data
  cp liwc_english_fix1.patch /usr/local/data
  cd /usr/local/data
  patch < liwc_english_fix1.patch
  python lexicons/dic2trie.py < LIWC2007_English100131.dic > liwc_2007.trie

Afterwards, you can adopt the usual workflow:

  from lexicons.liwc import Liwc
  liwc = Liwc()
  with open('/tmp/sample.txt', 'r') as document:
    summary = liwc.summarize_document(document.read())
    liwc.print_summarization(summary)

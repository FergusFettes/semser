# Semantic Scholar Search

Searches Semantic Scholar for papers or authors.

# Installation

```
pip install semser
```

or clone and install

```
git clone https://github.com/fergusfettes/semser
cd semser
pip install .
```

# Usage

```
$ semser "retrieval augmented generation"
1. Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks, Bob et al., 15 Nov 2019
...
Papers to retrieve: 1
Downloading
```

```
$ semser -a "Schmidhuber"
1. Jürgen Schmidhuber, 1 Jan 2015
...
Authors to retrieve: 1
1. Paper 1, 1 Jan 2015
2. Paper 2, 1 Jan 2015
Papers to retrieve: 1
Downloading
```

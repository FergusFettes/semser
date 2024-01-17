# Semantic Scholar Search

Searches Semantic Scholar for papers or authors. Downloads the papers as pdfs if they are on arxive.

# Installation

```
pip install semser
```

or clone and install

```
git clone https://github.com/fergusfettes/semser
cd semser
poetry install
```

# Usage

Search for some terms. You will get a list of papers to choose from.

```
$ semser search "retrieval augmented generation"
1. Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks, Bob et al., 15 Nov 2019
...
Papers to retrieve: 1
Downloading
```

Search for an author. You can select a likely looking author and you will be shown a selection of their papers.

```
$ semser author "Schmidhuber"
1. Jürgen Schmidhuber, 1 Jan 2015
...
Authors to retrieve: 1
1. Paper 1, 1 Jan 2015
2. Paper 2, 1 Jan 2015
Papers to retrieve: 1
Downloading
```

The 'limit' applies to authors and to papers by the author:
```
$ semser author "Schmidhuber" --limit 2
```

Will only return two papers by them. But you can grab their id and use it instead:

```
$ semser author 145341374 --limit 50
```

You can also search for a paper by its Semantic Scholar ID, or by its DOI, or just use the url from semantic scholar.

```
$ semser paper "10.1162/neco.1997.9.8.1735"
Downloading
```

Since it is made with typer, you can also just type
    
```
$ semser --help
$ semser search --help
```

to get a list of commands and options.

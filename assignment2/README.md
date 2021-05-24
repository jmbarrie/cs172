# CS172 - Assignment 2 (Retrieval)

### Team member 1 - Juan Barrientos

## Description

This is implemented using Python and the provided parsing code. It is broken down
into 3 classes (including assignment 1 classes):

1.  VectorSpaceModel
2.  IndexReader
3.  Ranker

The `VectorSpaceModel` class reads in the query file provided by users to create a tokenized vector model of the queries.

The `IndexReader` class is used to process user commands and retrieve
information from the documents created from the `build.py` script.
It is expanded further from assignment 1 by providing more complex
retrieval of information. Specifically, it searches through each term
of the provided queries and saves every document that a query term
belongs to. This is used later to determine the rank.

The `Ranker` class takes the information gathered in the
`IndexReader` which will then compute the cosine similarity using
binary weighting.

## Usage

All code is written in Python3 and the only external library is `PortStemmer` which is used for stemming.

To use this package it is a simple process:

1.  Build indexes
2.  Run queries using the a query list file

NOTE: It is assumed that all of these commands are executed from
inside the `/cs172/assignment2/` directory.

To build the required indexes, simply execute the `build.py` script. This will use the the `Tokenizer` and the `TermInfo` classes to build the required indexes.

`$ python build.py`

Once the `build.py` script has completed, queries can be executed
using the `VSM.py` script with a query list file and output file.

1.  `$ python ./VSM.py ./query_list.txt ./data/output.txt`

All queries should be executed as:

`$ python ./VSM.py [query file] [output file]`

Extra credit was not attempted for this assignment. And it is assumed
that because we used binary weighting to compute the cosine similarity
that the summation of term weights is equivalent to the sum of
multiple 1^2+1^2+...+1^2 values.

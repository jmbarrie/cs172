# CS172 - Assignment 1 (Tokenization)

### Team member 1 - Juan Barrientos

## Description
This inverted index is implemented using Python and the provided parsing code. It is broken down
into 3 classes: 

1.  Tokenizer
2.  TermInfo
3.  IndexReader

The `Tokenizer` class uses the provided `parsing.py` script to create the files: `term_index.txt`, `docids.txt`, and `termids.txt`.
These files can be found in the `/data/` directory after executing the `build.py` script.

The `TermInfo` class uses the documents created in the `Tokenizer` class to create the `term_info.txt` file. 
This file contains useful information for faster information retrieval from the `term_info.txt` file.

The `IndexReader` class is used to process user commands and retrieve information from the created documents.

## Usage
All code is written in Python3 and the only external library is `PortStemmer` which is used for stemming.

To use this package it is a simple process:

1.  Build indexes
2.  Run queries

NOTE: It is assumed that all of these commands are executed from inside the `/cs172/assignment1/` directory.

To build the required indexes, simply execute the `build.py` script. This will use the the `Tokenizer` and the `TermInfo` classes to build the required indexes.

`$ python build.py`

Once the `build.py` script has completed, queries can be executed using the `run_index.py` script. Some examples of queries are:

1.  `$ python ./read_index.py --term celluloid`
2.  `$ python ./read_index.py --doc AP890101-0001`
3.  `$ python ./read_index.py --doc AP890101-0001 --term celluloid`

All queries should be executed as:

`$ python ./read_index.py [command] [argument]`

Currently implemented commands are:

1. `--term [argument]`: returns information regarding the specified term.
2. `--doc [argument]`: returns information regarding the specified document.
3. `--doc [argument] --term [argument]`: returns information regarding the specified term found in the specified document.

Extra credit that was attempted: stemming and creation of documents. Both of these features can be found in the `Tokenizer` class. Stemming was implemented using `nltk`'s `PortStemmer`.

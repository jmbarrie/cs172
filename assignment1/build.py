'''
Main driver for the building the inverted index documents. Running this script will 
build the required indexes to use read_index.py. Four documents will be created in 
the './data/' directory:
1. docids.txt
2. term_index.txt
3. term_info.txt
4. termids.txt
'''
from src.tokenizer import Tokenizer
from src.terminfo import TermInfo

if __name__ == "__main__":
    tokenizer = Tokenizer()
    tokenizer.parse()
    term_info = TermInfo(['./data/term_index.txt', './data/term_info.txt'])
    term_info.create_term_info_dict()

import enum
import re
import os
import zipfile
import string

class Tokenizer:
    def __init__(self, zip_file=None):
        self.stop_words = self._create_stopwords()
        self.zip_file = zip_file
        self.doc_id = 0
        self.doc_id_dict = {}
        self.term_id = 0
        self.term_id_dict = {}
        self.corpus_index = {}
    
    def parse(self):
        # Regular expressions to extract data from the corpus
        doc_regex = re.compile("<DOC>.*?</DOC>", re.DOTALL)
        docno_regex = re.compile("<DOCNO>.*?</DOCNO>")
        text_regex = re.compile("<TEXT>.*?</TEXT>", re.DOTALL)

        if self.zip_file is not None:
            with zipfile.ZipFile(self.zip_file, 'r') as zip_ref:
                zip_ref.extractall()
        
        # Retrieve the names of all files to be indexed in folder ./ap89_collection_small of the current directory
        for dir_path, dir_names, file_names in os.walk("ap89_collection_small"):
            allfiles = [os.path.join(dir_path, filename).replace("\\", "/") for filename in file_names if (filename != "readme" and filename != ".DS_Store")]
            
        for file in allfiles:
            with open(file, 'r', encoding='ISO-8859-1') as f:
                filedata = f.read()
                result = re.findall(doc_regex, filedata)  # Match the <DOC> tags and fetch documents
                for document in result[0:]:
                    # Retrieve contents of DOCNO tag
                    docno = re.findall(docno_regex, document)[0].replace("<DOCNO>", "").replace("</DOCNO>", "").strip()
                    # Retrieve contents of TEXT tag
                    text = "".join(re.findall(text_regex, document))\
                            .replace("<TEXT>", "").replace("</TEXT>", "")\
                            .replace("\n", " ").lower().translate(str.maketrans('', '', string.punctuation))

                    # step 1 - lower-case words, remove punctuation, remove stop-words, etc. 
                    self._create_indexes(text, docno)
                    # step 2 - create tokens 
                    # step 3 - build index
        
        self._write_index_to_file(self.doc_id_dict, './data/docids.txt')
        self._write_index_to_file(self.term_id_dict, './data/termids.txt')
        self._write_corpus_index_to_file(self.corpus_index, './data/term_index.txt')

    @staticmethod
    def _write_corpus_index_to_file(index, file_name):
        with open(file_name, 'w') as f:
            for k, v in index.items():
                text = str(v[-1][2])
                for i in range(-1, len(v)):
                    text = text + f'\t%s:%s' % (v[i][-1], v[i][1])
            
                text = text + '\n'
                f.write(text)

    def _create_indexes(self, text, document):
        '''
        Creates the term index, doc index, and the corpus index then stores as member variables.
        '''
        position = 0

        for word in text.split():
            word_new_status = False

            if word not in self.stop_words:
                if word not in self.term_id_dict:
                    self.term_id_dict[word] = self.term_id
                    self.term_id += 1
                    word_new_status = True
            
                if document not in self.doc_id_dict:
                    self.doc_id_dict[document] = self.doc_id
                    self.doc_id += 1

                self.corpus_index.setdefault(word, []).append([self.doc_id_dict[document], position, self.term_id_dict[word]])

            position += 1

    @staticmethod
    def _write_index_to_file(index, file_name):
        if not os.path.exists('./data/'):
            os.mkdir('data')

        with open(file_name, 'w') as f:
            for k, v in index.items():
                text = f'%s\t%s\n' % (v, k) 
                f.write(text)

    def _create_stopwords(self):
        '''
        Creates stop words using the provided file.
        '''

        stop_words = []

        with open('stopwords.txt', 'r') as f:
            for line in f:
                stop_words.append(line.rstrip('\n'))

        return stop_words
    